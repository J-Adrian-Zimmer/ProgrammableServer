'''
The fileTools mixin contains

    fileOut -- which takes an absolute path name, guesses the
               mime type of that file from its extension, and
               sends that file to the browser

    read -- which reads a file in binary mode and returns its
            contents

    search -- which takes a partial path name beginning (assumed
              to begin with a subdirectory of the server or any
              application and searches for it in subdirectories
              in the appDirs list of expandableOrderings.json

              the search starts with the application whose 
              expander is currently executing and proceeds 
              towards the end of appDirs

              if there is no such application, the entire
              appDirs list is searched
'''


             

def mime_length(afile):
   from os.path import splitext,join
   from os import stat
   mtype = handler.extensions_map[
               splitext(afile)[1].lower()
           ]
   try:
      ln = stat(afile).st_size
   except:  
      (unmixed('out')).giveup(
        'fileTools.mime_length',
        500, 
        "Unrecognized internal file: " + afile
      )
   if mtype[:24]=='application/octet-stream':
      (unmixed('out')).giveup(
        'fileTools.mime_length',
        500, 
        "Unrecognized extension of internal file: "+afile
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
   if partialPath[0] in ['/','\\']: 
      partialPath = partialPath[1:]
   from os.path import exists,join
   for d in handler.server.soconsts.appDirs:
     fp = join(d,partialPath)
     if exists(fp): 
        return fp
   (unmixed('out')).giveup(
          'fileTools.search',
          500,
          'Could not find or read: ' + partialPath
   )
   # Note:  this search is not used to find 
   # expanders and expander mixins; to see
   # the code for that look at the load_mod
   # function in ProgrammableServer

def fileOut( absoluteName ):
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
     fileOut = fileOut
  )
