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
                               # for findng expander_mixins
from os.path import          basename,join
                               # do path manipulation
from config import           getList,postList,appDirs,debug
                               # lists are expander lists
                               # appDirs lists app dirs


def dbg(message,expanders=False):
  if debug==2:                 print(message)
  elif debug==1 and expanders: print(message)

class Handled (Exception): pass
    # because it is caught in do_GET and do_POST this
    # exception stops handler when handling is done


def giveup( handler, status, message ):
   # one of two ubiquitous functions
   # reports error to browser and stderr
   # see `error_message_format` in
   # https://docs.python.org/2/library/basehttpserver.html
   # to alter the look of the error screen
   dbg('giving up! |' + message + '|')
   handler.send_error(status,message)
   raise Handled()

def using(handler,mixin_tuple,where_dict):
   for name in mixin_tuple:
      loadMixin(handler,name,where_dict)

def server_init(server,serverRoot,serviceRoot):
   # wrap your BaseHTTPServer instance in this

   ## set directories ##
   global appDirs
   dbg( "serverRoot=" + serverRoot )
   appDirs.append(serverRoot)
   dbg( "appDirs=[" + ','.join(appDirs) + "]" )
  
   server._MEM = dict(
      want_continue = True,
      serverRoot = serverRoot,
      serviceRoot = serviceRoot,
      appDirs = appDirs,
      state = {}
   )

   ## finish the wrapping ##

   return server

def load_mod( handler, namepy, which ):
   # loads a module whose name we don't know at compile
   # time 
   # adds 'using' function to the module
   name = namepy[:-3] 
   dirs = map( lambda d: join(d,which), appDirs )
   try:
      fp, pathname, description = imp.find_module(
                         name,
                         dirs 
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
     dbg = lambda msg: dbg(msg,which=="expanders")
   ) )
   return m


def loadExpander(handler, expander_name ):
   dbg( "loading expander: " + expander_name )
   m = load_mod(
              handler, 
              expander_name+".py", 
              "expanders"
          )
   return m

def loadMixin(handler, mixin_name, where_dict):
   if handler._MEM.has_key(mixin_name):
      resources = handler._MEM[mixin_name]
   else:
      m = load_mod(
                 handler, 
                 mixin_name +".py", 
                 "expander_mixins"
      )
      resources = m.getResources(handler)
      handler._MEM[mixin_name] = resources
   where_dict.update(resources)
   dbg( 'loading mixin: ' + mixin_name )
   # dbg( ' installed are: ' + ','.join(resources.keys()) )

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

 
