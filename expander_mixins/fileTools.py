def ext2mime(afile):
   mtype = handler.extensions_map[
               splitext(afile)[1].lower()
           ]
   print '## ext2mime#' + mtype + '#'
   if mtype[:24]=='application/octet-stream':
      (unmixed('out')).giveup(
        'staticResponse.sendPublic',
        415, 
        "Unrecognized extension" 
      )
   return mtype

def readUtf8(absPath):
   try:
      from codecs import open
      with open(absPath,'r','utf-8') as fi:
          return fi.read()
   except:
      (unmixed('out')).giveup(
             'fileTools.readUtf8',
             500,
             'Disc read error'
      )
              

def readBinary(absPath):
   try:
      with open(absPath,'rb') as fi:
          return fi.read()
   except:
      (unmixed('out')).giveup(
             'fileTools.readBinary',
             500,
             'Disc read error'
      )

def pathSearch(partialPath):
  from os.path import exists
  for d in handler._MEM['earlyAPPS']:
     fp = normpath(join( d, partialpath ) )
     if exists(fp): return fp
  return None


