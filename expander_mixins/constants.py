'''
The constants expander mixin contains several values found in the
config.py file and/or set by the server when it starts up.  They 
should not be changed.
'''

def getResources():
   cs = handler.server.soconsts
   return dict (
     debug = cs.debug,
             # True or False
     unwanted_chars = cs.unwanted_chars,
             # for defanging upload paths
     localServe = cs.localServe,
             # True: browser on this computer only
             # False: browser anyplace than can reach here 
     port = cs.port,
             # listen port
     web_root= cs.web_root,
             # directory tree for static files
     server_dir = cs.server_dir,
             # directory where server is
     getList = cs.getList,
             # list of GET expanders in order tried
     postList = cs.postList,
             # list of POST expanders in order tried
     appDirs = cs.appDirs
             # list of applications in order tried
   )

