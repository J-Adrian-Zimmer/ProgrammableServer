"""
The upload mixin provides support for uploading files. 

  upload_template -- use to create a from for requesting
                     the upload; use this way
                       upload_template%(id,post_expander)


If loaded into a POST request environment, three other things
are provided

  upload  --  writes the uploaded file; single argument
              is an absolute file name to write to
  upload_file -- basename of the client's uploaded file
  upload_ext  -- extension of the client's uploaded file
                 (extension also included in the basename)

There is little flexibility here.  You must use the file form provided
by this mixin if the upload process is to work.  However, you can
control which expander receives the upload and use the form's id
to create CSS formatting for it.

This mixin makes use of undocumented properties of the FieldStorage
class in Python's cgi module.  It will be difficult to alter.
"""

import os,cgi

_error_msg = """ There has been a problem with the upload mixin.
Whether the problem was included in the HTML sent to the 
browser or in the server code is unknown."""

def _get_upload_info():
  # parse the upload request 
  # assume form followed our upload template
  try:
    data = cgi.FieldStorage(
               fp=handler.rfile,
               headers=handler.headers, 
               environ={
                'REQUEST_METHOD':
                  'POST', 
                'CONTENT_TYPE':
                  handler.headers['Content-Type'],
               }
           )
    return data['upfile']
  except:
    # get giveup and apply it
    (unmixed('out')).giveup( 
        'upload expander', 520, _error_msg
    )

def _upload_(upfile,writefilename): 
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
    if os.path.exists(writefilename): os.remove(writefilename)
    return False

def getResources():
   mixins("requestInfo")
   if command=='POST':
      ufile = _get_upload_info()
      return dict(
         upload_template = template,
         upload_filename = ufile.filename,
         upload_ext = os.path.splitext(ufile.filename)[1][1:],
         upload = lambda writename: _upload_(ufile,writename)
      )
   else:
      return dict(
         upload_template = template
      )




template = """
<form id="%s" action="%s" method="POST" enctype="multipart/form-data">
<input type="file" name="upfile"> <input type="submit" value="upload">
</form>
"""


