import os
join = os.path.join

def get():
  using('dirs', 'parsepath','send')
  ln2 = len(pathparts)==2

  def readFile():
     p = join(serverRoot, join(pathparts[0],pathparts[-1]))
     with open(p,'rb') as fi: return fi.read()
  
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
