usage = """
  python install.py programmable_server_dir
  
  Note current dir must be the dir for
   the app being installed.

  You can omit programmable_server_dir.
   If you do the it is assumed to be the 
   super dir of the current dir.
"""

import os, sys, shutil
join = os.path.join
exists = os.path.exists

## initiialize psdir and mydir ##

mydir = os.getcwd()

if len(sys.argv)==1: 
   psdir = os.path.normpath( join( mydir, '..' ) )
else:
   psdir = sys.argv[1]

if( not exists( join( psdir, 'serve.py' ) ) or
    not exists( join( mydir, 'install.py' ) )
  ):
   print(usage)
   sys.exit(1)
 

## get files.py

sys.path.append( join(psdir,'py') )
import files


## update expanderOrdering.json

dest_path = join(psdir,'expanderOrdering.json')
source = files.readJSON(join(mydir,'expanderOrdering.editable'))
dest   = files.readJSON(dest_path)
import json
try:
   dest.getList = \
     ['send_js_css'] + source.getList + dest.getList 
   dest.postList = source.postList + dest.postList
   dest.appDirs.insert(0,mydir)
except:
   print(
     "An expanderOrderings file is corrupted " +
     "in the server or in the application."        )
   sys.exit(1)

import json
files.writeJSON(dest_path,dest)

