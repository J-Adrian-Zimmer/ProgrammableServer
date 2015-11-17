#!/usr/bin/env python

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
join = os.path.join
from BaseHTTPServer import HTTPServer
from ProgrammableRequestHandler import \
     ProgrammableRequestHandler
import config

class Handled (Exception): pass
    # this exception stops ProgrammableRequestHandler
    # from trying more expanders

## helpers ##

class makeObj:
   def __init__(self, **kwds ):
        self.__dict__.update(**kwds)

def get_constants():
  import files

  jsobj = files.readJSON('expanderOrdering.json')


  ## adjust appDirs

  jsobj.appDirs.append(serverRoot)

  ## adjust getList

  if not config.listDir:
     jsobj.getList.append('nolist')
  if config.shutdown:
     jsobj.getList.append('shutdown')  

  return makeObj( 
     shutdown = _shutdown,
     Handled = Handled,
     
     debug = config.debug,
     localServe = config.localServe,
     port = config.port,
     jquery = config.jquery,
     web_root = None,
     set_web_root = setNewRoot,
     server_dir = serverRoot,
   
     getList = jsobj.getList,
     postList = jsobj.postList,
     appDirs = jsobj.appDirs

  )
  
def setNewRoot(new_path,obj):
   join = os.path.join
   isdir = os.path.isdir
   norm = os.path.normpath
  
   # if it's a dir accept it
   if isdir(new_path):
      obj.web_root = new_path
      return
   # if its public make it the server's directory 
   elif new_path=='public':
      obj.web_root = join( serverRoot, 'public')
      return

   # if it is relative attach it to the server's dir
   elif new_path[:3]=='../':
      apath = norm( join(server_dir, new_path ) )
      if os.path.isdir(apath): 
         obj.web_root = apath
      return

   # it ain't right
   raise Exception( 
     "web_root must be 'public', the path of a " +
     "directory relative to the server's " +
     " directory or abs path of a directory"
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


# enable module loading form the py directory

sys.path.append(join(serverRoot,'py') )


# setup constants
#    Please don't change these in your apps!
#    These will be asssigned to httpd.soconsts 
#    after we have a server.

consts = get_constants()
setNewRoot(config.web_root,consts)

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

print '\ngetList=' + str(','.join(consts.getList) + "\n")
print 'postList=' + str(','.join(consts.postList) + "\n")
print 'appDirs=' + str(','.join(consts.appDirs) + "\n")
print( 'Starting httpd on port '+ consts.port +
       ' and serving static files from ' + consts.web_root + "\n" )
print '...\n'

while want_continue: httpd.handle_request()

