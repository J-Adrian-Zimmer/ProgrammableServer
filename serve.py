import os,sys
from BaseHTTPServer import HTTPServer
from inspect import getsourcefile
from ProgrammableRequestHandler import ProgrammableRequestHandler, server_init
from config import localServe,web_root,upload_dir
join = os.path.join

## choose whether local or not ##
#  use port 80 anyway
 
server_address = ( ('127.0.0.1',80) if localServe 
                            else ('0.0.0.0',80) )


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


if upload_dir!='upload' and not os.path.isdir(upload_dir):
   raise Exception( 
   "upload_dir must be 'public' or abs path of a directory"
   )


# SimpleHTTPServer needs to have serviceRoot current
os.chdir(serviceRoot)  

# don't forget we must import stuff from serverRoot
sys.path.insert(1, serverRoot)

## allow expanders to import from py directory ##

sys.path.insert(1, join(serverRoot,'py') )


## setup the server ##
#  incl. _MEM['want_continue'] = True

httpd = server_init(
            HTTPServer(
               server_address, 
               ProgrammableRequestHandler
            ),   
            serverRoot,
            serviceRoot
        )


## run the server ##

print 'Starting httpd on port '+str(server_address[1])
print '...'

if localServe:
   while httpd._MEM['want_continue']: httpd.handle_request()
else:
   httpd.serve_forever() 


