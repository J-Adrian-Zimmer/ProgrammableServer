usage = """
usage: make_app_dir <absolute dir path>
"""

import sys, os, shutil

try:
  theDir = sys.argv[1]
except:
  print(usage)
  sys.exit(1)
if os.path.exists(theDir) and not os.path.isdir(theDir):
   print(usage)
   sys.exit(1)

join = os.path.join

def copyfile(name):
    shutil.copyfile(name,join(theDir,name))



if not os.path.exists(theDir): os.mkdir(theDir)

os.mkdir( join(theDir,"expanders") )
os.mkdir( join(theDir,"expander_mixins") )
os.mkdir( join(theDir,"css") )
os.mkdir( join(theDir,"js") )
os.mkdir( join(theDir,"upload") )
os.mkdir( join(theDir,"public") )

copyfile("config.py")
copyfile("install.py")


