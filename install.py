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
 


## initialize list of stuff to copy ## 

from installLists import \
   getList, postList, jsList, cssList, mixinList
list = { 'get' : getList,
         'post' : postList,
         'js' : jsList,
         'css' : cssList,
         'mixins' : mixinList
       }
listDirs = { 'get' : 'expanders',
             'post' : 'expanders',
             'js' : 'js',
             'css' : 'css',
             'mixins' : 'expander_mixins'
           }
lists = list.keys()


## maybe copy ##

if -f not in sys.argv: checkDups()

for sd in lists: copyList(sd)


## helper functions ##

def copyfile(name,subdir=''):
    shutil.copyfile(
              join(mydir,subdir,name),
              join(psdir,subdir,name)
    )

def copyList( n ):
   for f in list[n]: copyfile(f,listDir[n])

def checkDups():
   dups = []
   for n in lists:
      for f in list[n]:
          p = join(psdir,listDir[n],f)
          if exists( p ):
             dups.append(p)
   if len(dups)>0:
      print('These files are already installed.' +
            '  To copy over them, add the -f option.')
      for p in dups:
         print("  " + p )
      sys.exit(1)

