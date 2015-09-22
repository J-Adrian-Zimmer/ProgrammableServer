import os
join = os.path.join

def get():
  using('dirs', 'parsepath','send')
  ln2 = len(pathparts)==2

  def readFile():
     for d in appDirs:
        try:
           path = join( d, pathparts[0], pathparts[-1] )
           dbg('---trying--- ' + path)
           with open(path,'rb') as fi:  return fi.read()
        except:
           pass
     giveup(500,"cannot load " + pathparts[-1])
  
  if ln2 and pathparts[0]=='js':
     if pathext=='js':
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
  if ln2 and pathparts[0]=='css':
     if pathext=='css':
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
