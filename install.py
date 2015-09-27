usage = """
  python install.py programmable_server_dir
  
  Note current dir must be an app dir for
   the Programmable Server.

  If programmable_server_dir is omitted
   it is assumed to be the super dir of
   the current dir.
"""

import os, sys, shutil
join = os.path.join
exists = os.path.exists

## initiialize psdir and mydir ##

mydir = os.getcwd()

if len(sys.argv)==1: 
   psdir = os.normpath( join( mydir, '..' ) )
else
   psdir = sys.argv[1]

if( not exists( join( psdir, 'serve.py' ) or
    not exists.( join( myfile, 'install.py' ) 
  ):
   print(usage)
   sys.exit(1)
 

## inform expanderOrdering.py

dest_path = join(psdir,'expanderOrdering.json')
source = files.readJSON('expanderOrdering.json')
dest   = files.readJSON(dest_path)

dest.getList = source.getList ++ dest.getList
dest.postList = source.postList ++ dest.postList
dest.appDirs = dest.appDirs.insert(0,myDir)

files.writeJSON(dest_path)

