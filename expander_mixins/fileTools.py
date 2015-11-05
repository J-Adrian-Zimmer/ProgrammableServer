def mime_length(afile):
   from os.path import splitext
   mtype = handler.extensions_map[
               splitext(afile)[1].lower()
           ]
   if mtype[:24]=='application/octet-stream':
      (unmixed('out')).giveup(
        'fileTools.mime_length',
        415, 
        "Unrecognized extension" 
      )
   try:
     from os import stat
     ln = stat(afile).st_size
   except:  
      (unmixed('out')).giveup(
        'fileTools.mime_length',
        415, 
        "Unrecognized file: " + afile
      )
   return (mtype,ln)


def read(absPath):
   try:
      with open(absPath,'rb') as fi:
          return fi.read()
   except:
      (unmixed('out')).giveup(
             'fileTools.read',
             500,
             'File read error'
      )

def search(partialPath):
   from os.path import exists
   for d in handler._MEM['earlyApps']:
     fp = d +partialPath
     if exists(fp):
        return fp
   (unmixed('out')).giveup(
          'fileTools.search',
          500,
          'Could not find or read: ' + partialPath
   )

def file_out( absoluteName ):
  ct,cl = mime_length(absoluteName)
  (unmixed('out')).send(
    200,
    { 'content-type': ct,
      'content-length': cl
    },
    read( absoluteName )
  )

def getResources():
  return dict(
     search = search,
     read = read,
     mime_length = mime_length,
     file_out = file_out
  )
