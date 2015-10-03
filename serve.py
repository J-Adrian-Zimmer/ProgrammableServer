''' 
run server.py from the directory you found it in

configure it by editing config.py

restore default configurations by copying
  config.original to config.py

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
    # because it is caught in do_GET and do_POST this
    # exception stops handler when handling is done

## helpers  ##

class makeObj:
   def __init__(self, **kwds ):
        self.__dict__.update(**kwds)

def get_constants():
  import files
  from config import \
     localServe,web_root,port,multithreading,\
     unwanted_chars,debug

  jsobj = files.readJSON('expanderOrdering.json')
  def _dbg(message): print(message)
  def no_dbg(message): pass

  ## adjust web_root

  if web_root!='public' and not os.path.isdir(web_root):
    raise Exception( 
     "web_root must be 'public' or abs path of a directory"
    )

  if web_root=='public':
    web_root = os.path.normpath(
                     join( serverRoot, 'public')
               )

  if localServe.__class__.__name__=='bool': 
     def _no_response(x):
         return False;
  else:
     def _no_response(client_address):
        # only works for subnet 255.255.255.0 networks
        # with one gateway
        a,b = os.path.splitext(localServe)
        x,y = os.path.splitext(client_address)
        return a!=b or b==y

  ## add serverRoot to appDirs

  jsobj.appDirs.append(serverRoot)

  return makeObj( 
     shutdown = _shutdown,
     debug = debug,
     dbg = _dbg if debug>=1 else no_dbg,
     unwanted_chars = unwanted_chars,
     Handled = Handled,
     
     localServe = localServe,
     no_response = _no_response,
     port = port,
     multithreading = multithreading,
    
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
#        is to the same value.  This restriction
#        enables consistency in multithreading.


## setup server ##
 
serverAddress = ( ('127.0.0.1',int(consts.port))  \
                          if consts.localServe==True
                 else ('0.0.0.0',int(consts.port)) )

if consts.multithreading:
   from SocketServer import ThreadingMixIn
   class Server( ThreadingMixIn, HTTPServer ): pass
else:
   Server = HTTPServer

os.chdir(consts.web_root)  
#        SimpleHTTPServer needs serviceRoot to be current

httpd = Server(
            serverAddress, 
            ProgrammableRequestHandler
        )

httpd.soconsts = consts


## run the server ##

print 'Starting httpd on port '+ consts.port
print '...'

while want_continue: httpd.handle_request()

