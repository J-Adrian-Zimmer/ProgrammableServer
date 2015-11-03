'''
ProgrammableRequestHandler handles requests by executing
"expanders", in an order determined by declarations in 
'config.py' and until some expander actually handles the 
request. 
 
The tools expanders have to work with are provided by 
expander mixins.  Expanders attach mixins with the 'mixins' 
function.  

Each expander and expander mixin has two extra functions
mixed in: `mixins` and `giveup`; `giveup` handles a request
by sending and logging an error message. 

copyright 2015 by J Adrian Zimmer, MIT License
'''

import imp                     # need to import modules
                               # from string names
from SimpleHTTPServer import SimpleHTTPRequestHandler
                               # extending this
from os import               listdir
                               # for findng expander_mixins
from os.path import          basename,join,dirname,split
                               # do path manipulation
from urllib import unquote     # handler.path unquoted
                               # becomes request
from re import compile,match   # determinie acceptable
                               # paths
from urlparse import urlparse  # initializes _MEM

_okpath1 = r'(/[\w\d\-]+)*'
_okpath2 = r'(/([\w\d]\.|[\w\d\-])*$)'
okpath = compile(_okpath1+_okpath2)

class Bunch:
   '''
   The Bunch class makes a Python class from a dict
   It enable jsonIn to return an object rather than a dict
   '''
   def __init__(self, adict):
        self.__dict__.update(adict)

def giveup( handler, who, status, message, raiseHandled=True ):
   # reports error to browser and console
   msg = who + ' giving up!\n  |' + message + '|'
   print msg
   handler.send_error(status,msg)
   if raiseHandled:
      raise (handler.server.soconsts.Handled)()

def load_mod( handler, namepy, which ):
   # loads a module whose name we don't know at compile
   # time 
   # adds functions to its namespace
   name = namepy[:-3] 
   appDirs = handler.server.soconsts.appDirs
   dirs = map( 
            lambda d: join(d,which),
            appDirs[handler._MEM['start_search']:]
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
   try:
      if which=='expanders':
         handler._MEM['start_search'] = appDirs.index( 
                     split(dirname(m.__file__))[0] 
         )
   except:
      giveup(
         handler,
         'load_mod',
         500,
         'This simply should not happen.'
      )
   m.__dict__.update( dict( 
     mixins =  
       lambda *lst: mixins(handler,lst,m.__dict__),
     unmixed = 
       lambda mixinName: unmixed(handler,mixinName),
     
     handler = handler,
     Handled = handler.server.soconsts.Handled,
     
     request = handler._MEM['path'],
     debug =   handler.server.soconsts.debug
   ) )
   return m

def loadExpander(handler, expander_name ):
   handler._MEM['start_search'] = 0
   m = load_mod(
              handler, 
              expander_name+".py", 
              "expanders"
          )
   return m

def getMixin(handler, mixin_name):
   mix = handler._MEM['mixin']
   if mix.has_key(mixin_name):
      resources = mix[mixin_name]
      print '..fetched mixin: ' + mixin_name
   else:
      m = load_mod(
                 handler, 
                 mixin_name +".py", 
                 "expander_mixins"
      )
      resources = m.getResources()
      mix[mixin_name] = resources
      if debug:  print '..loaded mixin: ' + mixin_name
   return resources

def mixins(handler,mixin_tuple,where_dict):
   for name in mixin_tuple:
      where_dict.update( 
         getMixin(handler,name) 
      )

def unmixed(handler,mixinName):
   return Bunch( getMixin(handler,mixinName) )

def init_MEM(handler):
   global debug
   debug = handler.server.soconsts.debug

   scheme,netloc,path,params,query,fragment = \
                         urlparse(handler.path)
   
   if path!=r'/' and not match(okpath,path):
      giveup(handler,
             'init_MEM',
             404,
             'File Not Found: ' + handler.path
             ) 
   
   
   
   handler._MEM = { 
           'start_search':None,
              # the server's directory is at this index
           'mixin':{},
           'scheme':scheme,
           'netloc':netloc,
           'path':path,
           'params':params,
           'query':query,
           'headers':handler.headers
   }

class ProgrammableRequestHandler(SimpleHTTPRequestHandler):
    
    def do_GET(self):
      init_MEM(self)
      if not unmixed(self,'network').serve():
         return
      if debug: 
         print "GET REQUEST PATH:\n  " + self._MEM['path']
      try:
         for n in self.server.soconsts.getList:
            if debug:  print( 'TRYING: ' + n )
            loadExpander(self,n).get()
         if debug:  print('Starting SimpleHTTPRequestHandler')
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
      init_MEM(self)
      if not unmixed(self,'network').serve():
         return
      if debug: 
         print "POST REQUEST PATH:\n  " + self._MEM['path']
      try:
         for n in self.server.soconsts.postList:
            if debug: print('TRYING ' + n)
            loadExpander(self,n).post()
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


