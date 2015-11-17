usage = """
usage: make_app_dir <absolute dir path>
"""

import sys, os, shutil
join = os.path.join
sys.path.append('py')

import files

## helpers ##

def copyfile(name,subdir='',subdir2=None):
    subdir2 = subdir2 or subdir
    shutil.copyfile(
              join(subdir,name),
              join(theDir,subdir2,name)
    )

## end helpers ##

## initialize theDir ##

try:
  theDir = sys.argv[1]
except:
  print(usage)
  sys.exit(1)
if os.path.exists(theDir) and not os.path.isdir(theDir):
   print(usage)
   sys.exit(1)

## make the directory tree ##

if not os.path.exists(theDir): os.mkdir(theDir)

os.mkdir( join(theDir,"expanders") )
os.mkdir( join(theDir,"expander_mixins") )
os.mkdir( join(theDir,"css") )
os.mkdir( join(theDir,"js") )

## add a few files ##

files.writeJSON(
      join(theDir,"expanderOrdering.editable"),
      { 'getList':[],
        'postList':[]
      }  ) 

copyfile("install.py",'py','.')
copyfile("__init__.py","expanders")
copyfile("__init__.py","expander_mixins")



