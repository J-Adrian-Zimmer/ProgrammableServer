import os,sys
from BaseHTTPServer import HTTPServer
from inspect import getsourcefile
from ProgrammableRequestHandler import \
     ProgrammableRequestHandler, server_init
from config import \
     localServe,web_root,port,multithreading
join = os.path.join

## choose whether local or not ##
 
server_address = ( ('127.0.0.1',int(port))  \
                            if localServe==True
                            else ('0.0.0.0',int(port)) )


## get serviceRoot and serverRoot right ##

serverRoot = os.path.dirname(getsourcefile(server_init))
#            need to know where our server is located


if web_root!='public' and not os.path.isdir(web_root):
   raise Exception( 
   "web_root must be 'public' or abs path of a directory"
   )

if web_root=='public':
   serviceRoot = os.path.normpath(
                    os.path.join(
                        serverRoot,
                        web_root
                 )  )
else:
   serviceRoot = web_root

## Arrange for multithreading or not ##

if multithreading:
   from SocketServer import ThreadingMixIn
   class Server( ThreadingMixIn, HTTPServer ): pass
else:
   Server = HTTPServer

# SimpleHTTPServer needs to have serviceRoot current
os.chdir(serviceRoot)  

# don't forget we must import stuff from serverRoot
sys.path.insert(1, serverRoot)

## setup the server ##
#  this will establish _MEM['want_continue'] = True

httpd = server_init(
            Server(
               server_address, 
               ProgrammableRequestHandler
            ),   
            serverRoot,
            serviceRoot
        )


## run the server ##

print 'Starting httpd on port '+ port
print '...'

if localServe:
   while httpd._MEM['want_continue']: httpd.handle_request()
else:
   httpd.serve_forever() 

## helper functions

def make_installed_config
