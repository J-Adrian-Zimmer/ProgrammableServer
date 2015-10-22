#!/usr/bin/env python
# -*- coding: latin-1 -*-

# Running Python from $PATH, it had better be Python 2.7.x

''' 
run server.py from the directory you found it in

configure it by editing config.py

restore default configurations running restore.py

install apps by running install.py from
  the directory that contains  the app
'''

## imports ##

import os,sys
from BaseHTTPServer import HTTPServer
from ProgrammableRequestHandler import \
     ProgrammableRequestHandler
join = os.path.join

class Handled (Exception): pass
    # this exception stops ProgrammableRequestHandler
    # from trying more expanders

## helpers ##

class makeObj:
   def __init__(self, **kwds ):
        self.__dict__.update(**kwds)

def get_constants():
  import files, config

  jsobj = files.readJSON('expanderOrdering.json')

  if config.localServe.__class__.__name__=='bool': 
    def _no_response(forget_it):
         return config.localServe.__class__.__name__

  else:
    def _no_response(client_address):
        # only works for subnet 255.255.255.0 networks
        # with one gateway
        a,b = os.path.splitext(config.localServe)
        x,y = os.path.splitext(client_address)
        print "client_address=" + client_address
        return (client_address!='127.0.0.1' and
                (a!=x or b==y) 
               )


  ## assign web_root

  if ( config.web_root=='public' ):
    web_root = os.path.normpath(
                     join( serverRoot, 'public')
               )
  elif( os.path.isdir(config.web_root) ):
    web_root = os.path.normpath(config.web_root)
  else:
    raise Exception( 
     "web_root must be 'public' or abs path of a " +
     "directory\n check your config.py file"
    )

  ## adjust appDirs

  jsobj.appDirs.append(serverRoot)

  ## adjust getList

  if not config.listDir:
     jsobj.getList.append('nolist')
  if config.shutdown:
     jsobj.getList.append('shutdown')  

  return makeObj( 
     shutdown = _shutdown,
     debug = config.debug,
     unwanted_chars = config.unwanted_chars,
     Handled = Handled,
     
     localServe = config.localServe,
     no_response = _no_response,
     port = config.port,
    
     web_root= web_root,
     server_dir = serverRoot,
   
     getList = jsobj.getList,
     postList = jsobj.postList,
     appDirs = jsobj.appDirs,

  )
  

def check_where_we_are():
   fs = os.listdir(serverRoot)
   if not( 'ProgrammableRequestHandler.py' in fs and
           'serve.py' in fs and
           'config.py' in fs
      ):
     raise Exception(
        "ProgrammableServer's own directory must be current!"
     )

want_continue = True

def _shutdown():
  global want_continue
  want_continue = False


## end Helper Functions ##


## setup serverRoot and imports ##

serverRoot = os.getcwd()

check_where_we_are()

sys.path.append(serverRoot)
sys.path.append(join(serverRoot,'py') )

consts = get_constants()
#        Renamed httpd.soconsts after we have a server.
#        Think of soconsts as constants (sort of)
#        They may be changed if any possible change
#        is to the same value.  


## setup server ##
 
serverAddress = ( ('127.0.0.1',int(consts.port))  \
                          if consts.localServe==True
                 else ('0.0.0.0',int(consts.port)) )

os.chdir(consts.web_root)  
#        SimpleHTTPServer needs web_root to be current
#        directory

httpd = HTTPServer(
            serverAddress, 
            ProgrammableRequestHandler
        )

httpd.soconsts = consts


## run the server ##

print 'getList=' + str(','.join(httpd.soconsts.getList))
print( 'Starting httpd on port '+ consts.port +
       ' and serving static files from ' + consts.web_root )
print '...'

while want_continue: httpd.handle_request()

