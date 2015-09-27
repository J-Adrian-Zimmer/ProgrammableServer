import os
join = os.path.join

def get():
  using('basic', 'orderings', 'details')
  ln2 = len(path)==2

  def readFile():
     dbg('send_js_css reading: ' + path[-1] + ' from ' + path[0] )
     for d in appDirs:
        try:
           fp = join( d, path[0], path[-1] )
           with open(fp,'rb') as fi:  return fi.read()
        except:
           pass
     giveup(500,"cannot load " + path[-1])
  
  if ln2 and path[0]=='js':
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
  if ln2 and path[0]=='css':
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
