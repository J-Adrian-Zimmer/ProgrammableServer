import os
join = os.path.join

def get():
  mixins(
         'out',         # for send and giveup
         'constants',   # for appDirs
         'requestInfo'  # for  path, and pathext
      )
  print 'ONE:'  + str(len(path))
  ln2 = len(path)==2
  if len(path)>1:  print path[0] + '///' + path[1]
  def readFile():
     for d in appDirs:
        try:
           fp = join( d, path[0], path[-1] )
           with open(fp,'rb') as fi:  return fi.read()
        except:
           pass
     giveup(
        'send_js_css 1', 
        500,
        "cannot load " + path[-1]
     )
 
  try:
     if ln2 and path[0]=='js':
        if pathext=='js':
           send(
              200,
              {'content-type':'text/js',
               'cache-control':'max-age=10,must-revalidate'
              },
              readFile()
           )
        else:
           giveup(
              'send_js_css 2', 
              404,
              "Expecting a 'js' file"
           )
     if ln2 and path[0]=='css':
        if pathext=='css':
           send(
              200,
              {'content-type': 'text/css',
               'cache-control':'max-age=10,must-revalidate'
              },
              readFile()
           )
        else:
           giveup(
              'send_js_css 3', 
              404,
              "Expecting a 'css' file"
           )
     print 'TWO'
  except handler.server.soconsts.Handled:
     raise Handled()
  except Exception as e:
     giveup(
        'send_js_css 4', 
        500,
        e.message
     )
     
       
