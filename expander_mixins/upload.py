'''
The upload mixin provides some html for a file form to GET requests.

For POST requests it also provides a method to receive uploaded
files and references to strings giving the uploaded file's name
and extensions.

There is little flexibility here.  You must use the file form provided
by this mixin if the upload process is to work.  However the form
is given in a template which you can adapt.  Use it this way

   upload_template % (id, action_url)

where id is an id you can reference in css and the action url
lets you decide which expander will respond to the upload.
'''

import os, cgi

_error_msg = """ There has been a problem with the upload mixin.
Whether the problem was included in the HTML sent to the 
browser or in the server code is unknown."""

def _get_upload_info(handler):
  # parse the upload request 
  # assume form followed our upload template
  try:
    form = cgi.FieldStorage(
               fp=handler.rfile,
               headers=handler.headers, 
               environ={
                   'REQUEST_METHOD':'POST', 
                   'CONTENT_TYPE':handler.headers['Content-Type'], 
               }
           )
    return form['upfile']
  except:
    giveup( 520, _error_msg )

def _upload_(upfile,writefilename): 
  # write the file to the upload directory and
  # return a success boolean
  try: 
    with open(writefilename, 'wb') as fo:
       while True:
          chunk = upfile.file.read(8192)
          if len(chunk) == 0:
              break
          else:
              fo.write(chunk)
       return True
  except Exception as e:
    dbg( 'From upload.py: ' + e.message )
    if os.path.exists(writefilename): os.remove(writefilename)
    return False

def getResources(handler):
   using("inparameters")
   if command=='POST':
      ufile = _get_upload_info(handler)
      return dict(
        
         # upload_template is a <form> tag 
         # use with % (id,action_url) 
         upload_template = template,

         # upload_filename is basename of the 
         # file to be uploaded
         upload_filename = ufile.filename,

         # upload_ext is the extension of upload_filename 
         upload_ext = os.path.splitext(ufile.filename)[1][1:],

         # upload a file and store it in the upload directory
         # using the basename of the argument
         upload = (
            lambda writename: _upload_(ufile,writename)
         )
      
      )
   else:
      return dict(
         # upload_template is a <form> tag 
         # use with % (id,action_url) 
         upload_template = template

      )




template = """
<form id="%s" action="%s" method="POST" enctype="multipart/form-data">
<input type="file" name="upfile"> <input type="submit" value="upload">
</form>
"""

