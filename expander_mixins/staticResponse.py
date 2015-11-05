'''
The staticResponse mixin allows static files to be served from outside the web_root directory tree.  There are two functions.  Both either do their thing and raise Handled or have no effect.  Their thing can include an error response. 
 
      sendPublic(filepath)
               --  looks for filepath in the server's 
                   public directory tree  
                   
                   if found sends it to the browser and 
                   raises Handled
                   
                   useful when web_root is shifted from 
                   'public'

      sendSearch(filepath,subdir)
                -- looks for filepath in one of the subdir
                   directories (searching through apps in 
                   reverse order of installation and then 
                   the server dir)

                   subdir must be the existing file
                   extension and suitable for a 
                   "text/<subdir>" mimetype
                    
                   if found sends it to the browser and 
                   raises Handled

                   useful for the js and css file override 
                   system

Notice that filepath is not defanged.  Don't put user or browser
obained data in it without defanging.  (Using the path array in
the requestInfo expander mixin is one way of doing this.)
'''


def sendPublic(filepath):
   if filepath[0]=='/': filepath = filepath[1:]
   import os
   from os.path import join, splitext, normpath
   mixins('out')
   afile = normpath(join(
             (unmixed('constants')).server_dir,
             'public',
             filepath
           ))
   try:
      with open( afile, 'rb') as fo: page = fo.read()
      page_len = os.stat(afile).st_size
   except:
      (unmixed('out')).giveup(
        'staticResponse.sendPublic',
        404, 
        "Cannot find readable version of " + filepath 
      )
    
   mtype = handler.extensions_map[
               splitext(afile)[1].lower()
           ]
   if mtype[:24]=='application/octet-stream':
      (unmixed('out')).giveup(
        'staticResponse.sendPublic',
        415, 
        "Unrecognized extension" 
      ) 
   else:
      _respond(mtype,page,page_len)

def sendSearch(filepath,subdir):
  from os.path import join, normpath
  import os
  mixins('requestInfo')
  print pathext + '==' + subdir
  if pathext!=subdir:
     (unmixed('out')).giveup(
                 "staticSearch.sendsearch",
                 500,
                 "Unexpected file extension"
     )
  content = None
  for d in (unmixed('constants').appDirs):
     try:
        fp = normpath(join( d, subdir, path[-1] ))
        with open(fp,'rb') as fi:  content = fi.read()
        content_len = os.stat(fp).st_size
     except:
        pass
  if content:
     _respond(
         "text/%s" % subdir, 
         content,
         content_len
     )
  else:
     (unmixed('out')).giveup(
        'staticResponse._findFile', 
        500,
        "cannot load " + findFile 
     )


def _respond(mtype,content,numbytes):
      handler.send_response(200)
      handler.send_header( "content-type", mtype )
      handler.send_header( 
         'content-length', str(numbytes) 
      )
      handler.end_headers()
      handler.wfile.write(content)
      raise Handled

def getResources():
   return dict( 
       sendPublic = sendPublic,
       sendSearch = sendSearch
   )
