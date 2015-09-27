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
from config import           debug


def dbg(message,expanders=False):
  if debug==2:                 print(message)
  elif debug==1 and expanders: print(message)


def giveup( handler, who, status, message ):
   # reports error to browser and console
   msg = who + ' giving up!\n  |' + message + '|'
   print(msg)
   handler.send_error(status,msg)
   raise handler.Handled()

def using(handler,mixin_tuple,where_dict):
   dbg( 'using: ' + ';'.join(mixin_tuple) )
   for name in mixin_tuple:
      loadMixin(handler,name,where_dict)


def load_mod( handler, namepy, which ):
   # loads a module whose name we don't know at compile
   # time 
   # adds 'using' function to the module
   name = namepy[:-3] 
   dirs = map( 
            lambda d: join(d,which), 
            handler.server.soconsts.appDirs 
          )
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
        'load_mod',
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
   m = load_mod(
              handler, 
              expander_name+".py", 
              "expanders"
          )
   dbg( "loaded expander: " + expander_name ) 
   return m

def loadMixin(handler, mixin_name, where_dict):
   mix = handler._MEM['mixin']
   if mix.has_key(mixin_name):
      resources = mix[mixin_name]
   else:
      m = load_mod(
                 handler, 
                 mixin_name +".py", 
                 "expander_mixins"
      )
      resources = m.getResources(handler)
      mix[mixin_name] = resources
   where_dict.update(resources)

class ProgrammableRequestHandler(SimpleHTTPRequestHandler):
    
    def do_GET(self):
      dbg( "\n\n\n\n" + self.path )
      self._MEM = { 'mixin':{} }
      self.Handled = self.server.soconsts.Handled
      try:
         for n in self.server.soconsts.getList:
            loadExpander(self,n).get()
         SimpleHTTPRequestHandler.do_GET(self)
      except self.Handled:
         pass  # Handled means browser and (if necessary)
               # log have been informed
      except Exception as e:
         giveup( self, 
                 'do_GET (with ' + n + ')', 
                 500, 
                 e.message
               )
            

    def do_POST(self):
      dbg( "\n\n\n\n" + self.path )
      self._MEM = { 'mixin':{} }
      self.Handled = self.server.soconsts.Handled
      try:
         for n in self.server.soconsts.postList:
            loadExpander(self,n).post()
         path = self.path.split('?')[0]
         giveup(self, 404, 'do_POST', path+' not available')
      except self.Handled:
         pass  # Handled means browser and (if necessary)
               # log have been informed
      except Exception as e:
         giveup( self, 
                 'do_POST (with ' + n + ')', 
                 500, 
                 e.message
               )

 
