'''
The js_css mixin responds to requests for .js files from the js
subdirectory and .css files from the css subdirectory.
'''

import os
join = os.path.join

def readFile():
   using('dirs')
   for d in appDirs:
      try:
         path = join( d, pathparts[-1] )
         with open(path,'rb') as fi:  return fi.read()
      except:
         pass
   giveup(500,"Cannot load " + pathparts[-1])


def get():
  using('parsepath','send')
  if len(pathparts)==2 and pathparts[0].lower()=='js':
     if pathext.lower()=='js':
        send(
           200,
           {'content-type':'text/js' },
            readFile()
        )
     else:
        giveup(
           404,
           "Expecting a 'js' file"
        )
  if len(pathparts)==2 and pathparts[0].lower()=='css':
     if pathext.lower()=='css':
        send(
           200,
           {'content-type': 'text/css'},
            readFile()
        )
     else:
        giveup(
           404,
           "Expecting a 'css' file"
        )
