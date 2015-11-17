'''
The constants expander mixin contains several values found in the
config.py file and/or set by the server when it starts up.  They 
should not be changed.
'''

def getResources():
   sc = handler.server.soconsts
   return dict (
     debug = sc.debug,
             # True or False
     localServe = sc.localServe,
             # True: browser on this computer only
             # False: browser anyplace than can reach here 
     port = sc.port,
             # listen port
     server_dir = sc.server_dir,
             # directory where server is
     web_root = sc.web_root,
             # starts out as the public subdir of
             # the server dir
             # then, maybe, reset by set_web_root
     set_web_root = \
        lambda new_root: sc.set_web_root( new_root, sc ),
             # redefine the web_root; can be "public"
             # relative to server_dir or absolute
     jquery = sc.jquery
             # where jQuery will be fetched from
   )

