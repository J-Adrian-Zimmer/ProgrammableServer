usage = '''
usage: python restore()
       (Execute from the ProgrammableServer dir.)
'''

import os, shutil, json

## initialize psdir ##

psdir = os.getcwd()

if not exists.( join( myfile, 'install.py' ) ):
   print(usage)
   sys.exit(1)

## clear all installed stuff ##

for d in [ join(psdir,'expanders'),
           join(psdir,'expander_mixins'),
           join(psdir,'js'),
           join(psdir,'css')
         ]:
   clearDir(d)

with open(join(psdir,'expanderOrdeering.json'), 'w') as fo:
   fo.write(
      json.dumps( 
         {'getList':[], 'putList':[]}
   )  )


## install the basic app ##

os.chdir( join(psdir,'basic_app') )
execfile('install.py')


## helper functions ##

def clearDir(dir):
   shutil.rmtree(dir)
   os.mkdir(dir)


