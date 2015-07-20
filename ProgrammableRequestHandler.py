'''
ProgrammableRequestHandler handles requests by executing
"expanders", in an order determined by declarations in 
'config.py' and until some expander actually handles the 
request. 
 
The tools expanders have to work with are provided by 
expander mixins.  Expanders attach mixins with the 'using' 
function.  

Each expander and expander mixin has two extra functions
mixed in: `using` and `giveup`; `giveup` handles a request
by sending and logging an error message. 

copyright 2015 by J Adrian Zimmer, MIT License
'''

import imp                     # need to import modules
                               # from string names
from SimpleHTTPServer import SimpleHTTPRequestHandler
                               # extending this
from os import               listdir
                               # findng expander_mixins
from os.path import          basename,join
                               # do path manipulation
from config import           getList,postList
                               # expander lists

mixin_dir = None    # set in server_init
expander_dir = None     # set in server_init


def dbg(message):
   # change the comment if you do or do not want
   # to see debug output -- dbg is included in
   # expanders and expander mixins

   pass

   # print(message)

class Handled (Exception): pass
    # because it is caught in do_GET and do_POST this
    # exception stops handler when handling is done


def giveup( handler, status, message ):
   # one of two ubiquitous functions
   # reports error to browser and stderr
   # see `error_message_format` in
   # https://docs.python.org/2/library/basehttpserver.html
   # to alter the look of the error screen
   handler.send_error(status,message)
   raise Handled()

def using(handler,mixin_tuple,where_dict):
   for name in mixin_tuple:
      loadMixin(handler,name,where_dict)

def server_init(server,serverRoot,serviceRoot):
   # wrap your BaseHTTPServer instance in this

   ## set directories ##
   global mixin_dir, expander_dir
   dbg( "serverRoot=" + serverRoot )
   mixin_dir = join( serverRoot, 'expander_mixins' )
   expander_dir = join( serverRoot, 'expanders')
  
   ## get list of mixins ##
   
   server._MEM = dict(
      want_continue = True,
      serverRoot = serverRoot,
      serviceRoot = serviceRoot,
      state = {}
   )

   ## finish the wrapping ##

   return server

def load_mod( handler, namepy, path ):
   # loads a module whose name we don't know at compile
   # time 
   # adds 'using' function to the module
   name = namepy[:-3] 
   try:
      fp, pathname, description = imp.find_module(
                         name,
                         [ path ]
                      )
      try:
          m = imp.load_module(
                     name, fp, pathname, description
                 )
      finally:
          if fp: fp.close()
   except:
      giveup(
        handler,
         500, 
        'could not load ' + namepy,
      )
     
   m.__dict__.update( dict( 
     using =  
       lambda *lst: using(handler,lst,m.__dict__),
     dbg = dbg
   ) )
   return m


def loadExpander(handler, expander_name ):
   dbg( "LOADING EXPANDER:" + expander_name )
   m = load_mod(
              handler, 
              expander_name+".py", 
              expander_dir
          )
   return m

def loadMixin(handler, mixin_name, where_dict):
   if handler._MEM.has_key(mixin_name):
      resources = handler._MEM[mixin_name]
   else:
      m = load_mod(
                 handler, 
                 mixin_name +".py", 
                 mixin_dir
      )
      resources = m.getResources(handler)
      handler._MEM[mixin_name] = resources
   where_dict.update(resources)
   dbg( 'for ' + mixin_name + ' installed are: ' +
        ','.join(resources.keys()) )

class ProgrammableRequestHandler(SimpleHTTPRequestHandler):
    
    def do_GET(self):
      dbg( "\n\n\n\n" + self.path )
      self._MEM = {}
      self.Handled = Handled
      try:
         for n in getList: 
            loadExpander(self,n).get()
         SimpleHTTPRequestHandler.do_GET(self)
      except Handled:
         pass  # Handled means browser and (if necessary)
               # log have been informed
      except Exception as e:
         giveup( self, 500, e.message ) 
            

    def do_POST(self):
      dbg( "\n\n\n\n" + self.path )
      self._MEM = {}
      self.Handled = Handled
      try:
         for n in postList: 
            loadExpander(self,n).post()
         path = self.path.split('?')[0]
         giveup(self,404, path + ' not available')
      except Handled:
         pass  # Handled means browser and (if necessary)
               # log have been informed
      except Exception as e:
         giveup( self, 500, e.message )

 
