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
from SocketServer     import StreamRequestHandler
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
   #print( "loaded expander: " + expander_name ) 
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
      resources = m.getResources()
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

## set up handler queue ##

def do_get(handler):
   if handler.server.soconsts.no_response(
            handler.client_address[0][:9]
   ): return
   init_MEM(handler)
   try:
      for n in handler.server.soconsts.getList:
         print('get>>>' + n)
         loadExpander(handler,n).get()
      print('<<<get')
      try:
         SimpleHTTPRequestHandler.do_GET(handler)
         raise handler.server.soconsts.Handled
      except Exception as e:
         print "SimpleHTTP problem: "  + e.message
         giveup( handler, "SimpleHTTPRequestHandler",500,e.message)
      print('Done with SimpleHTTPRequestHandler')
   except handler.server.soconsts.Handled:
      pass  # Handled means browser and (if necessary)
            # log have been informed
   except Exception as e:
      print 'the do_get Exception ||' + e.message + '||'
      giveup( handler, 
              'do_GET (with ' + n + ')', 
              500, 
              e.message,
              False
            )
   finally:
      StreamRequestHandler.finish(handler)
      print "!!Finished the Handler Off!!"
            
def do_post(handler):
   if handler.server.soconsts.no_response(
            handler.client_address[0][:9]
   ): return
   init_MEM(handler)
   print "POST => " + handler.path
   try:
      for n in handler.server.soconsts.postList:
         print 'STARTING WITH ' + n
         loadExpander(handler,n).post()
         print 'DONE WITH ' + n
      dbg('<<<post')
      giveup(
         handler, 
         'do_POST', 
         404, 
         handler._MEM['path'] + ' not available'
      )
   except handler.server.soconsts.Handled:
      pass  # Handled means browser and (if necessary)
            # log have been informed
   except Exception as e:
      giveup( handler, 
              'do_POST (with ' + n + ')', 
              500, 
              e.message,
              False
            )
   finally:
      StreamRequestHandler.finish(handler)


