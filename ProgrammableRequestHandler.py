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
# other imports in def dbg and def init_MEM


def dbg(message): pass
    # maybe redefined in init_MEM

def giveup( handler, who, status, message, raiseHandled=True ):
   # reports error to browser and console
   msg = who + ' giving up!\n  |' + message + '|'
   print msg
   handler.send_error(status,msg)
   if raiseHandled:
      raise (handler.server.soconsts.Handled)()

def using(handler,mixin_tuple,where_dict):
   dbg( 'using: ' + ';'.join(mixin_tuple) )
   for name in mixin_tuple:
      loadMixin(handler,name,where_dict)


def load_mod( handler, namepy, which ):
   # loads a module whose name we don't know at compile
   # time 
   # adds 'using' function to the e
   name = namepy[:-3] 
   dirs = map( 
            lambda d: join(d,which), 
            handler.server.soconsts.appDirs 
          )
   dbg("loading " + name + ":" + ';'.join(dirs))
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
     request = handler._MEM['path'],
     handler = handler,
     Handled = handler.server.soconsts.Handled
   ) )
   return m


def loadExpander(handler, expander_name ):
   m = load_mod(
              handler, 
              expander_name+".py", 
              "expanders"
          )
   #dbg( "loaded expander: " + expander_name ) 
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
   #dbg( "loaded expander_mixin: " + mixin_name )

def init_MEM(handler):
   global dbg
   if handler.server.soconsts.debug==2:
      def _dbg(msg): print msg 
      dbg = _dbg
   import urlparse
   
   scheme,netloc,path,params,query,fragment = \
                 urlparse.urlparse(handler.path)
   
   handler._MEM = { 
           'mixin':{},
           'scheme':scheme,
           'netloc':netloc,
           'path':path,
           'params':params,
           'query':query,
           'fragment':fragment,
           'headers':handler.headers
   }
   dbg("init_MEM FINISHED")

class ProgrammableRequestHandler(SimpleHTTPRequestHandler):
    
    def do_GET(self):
      if self.server.soconsts.no_response(
               self.client_address[0][:9]
      ): return
      dbg( "GET => " + self.path )
      init_MEM(self)
      try:
         for n in self.server.soconsts.getList:
            loadExpander(self,n).get()
         dbg('<<<get')
         SimpleHTTPRequestHandler.do_GET(self)
      except self.server.soconsts.Handled:
         pass  # Handled means browser and (if necessary)
               # log have been informed
      except Exception as e:
         giveup( self, 
                 'do_GET (with ' + n + ')', 
                 500, 
                 e.message,
                 False
               )
            
    def do_POST(self):
      if self.server.soconsts.no_response(
               self.client_address[0][:9]
      ): return
      init_MEM(self)
      print "POST => " + self.path
      try:
         for n in self.server.soconsts.postList:
            print 'STARTING WITH ' + n
            loadExpander(self,n).post()
            print 'DONE WITH ' + n
         dbg('<<<post')
         giveup(
            self, 
            'do_POST', 
            404, 
            self._MEM['path'] + ' not available'
         )
      except self.server.soconsts.Handled:
         pass  # Handled means browser and (if necessary)
               # log have been informed
      except Exception as e:
         giveup( self, 
                 'do_POST (with ' + n + ')', 
                 500, 
                 e.message,
                 False
               )


