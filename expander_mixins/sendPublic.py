'''
Provides one function, sendP, which will send a page from the
server's public directory.  This is useful when web_root is
set to something else.
'''

def _send(filename):
   if filename[0]=='/': filename = filename[1:]
   print 'SENDP:' + filename
   from os.path import join, splitext
   mixins('out')
   afile = join(
             (unmixed('constants')).server_dir,
             filename
           )
   try:
      print 'OPENING:' + afile
      with open( afile, 'rb') as fo: 
          page = fo.read()
   except:
      giveup( 
        'sendPublic',
        404, 
        "Cannot find readable version of " + filename 
      )
   print 'THE EXTENSION:' + splitext(afile)[1].lower() + ':'
    
   mtype = handler.extensions_map[
               splitext(afile)[1].lower()
           ]
   if mtype[:24]=='application/octet-stream':
      giveup( 
        'sendPublic',
        415, 
        "Unrecognized extension" 
      ) 
   else:
      if mtype[:4]=='text': 
         page = page.encode('utf-8')
         mtype = mtype + '; charset=utf-8'
      handler.send_response(200)
      handler.send_header( "content-type", mtype )
      handler.send_header( 
         'content-length', str(len(page)) 
      )
      handler.end_headers()
      handler.wfile.write(page)
      raise Handled

def getResources():
   return dict( sendP = _send )
