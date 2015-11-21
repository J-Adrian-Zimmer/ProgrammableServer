"""
The upload mixin provides support for uploading files. 

   upload_template -- names the following boiler plate:
         
     <input type="file" id="upload--file-name"> 
     <button id="upload--submit">submit upload</button>
         
     Note: You will need these id's in your expanders!
           They are immutable because hard coded into
           support.js as well.


If loaded into a POST request environment, three other things
are provided

  upload  --  writes the uploaded file; the single argument
              is an absolute file name to write to
  upload_filename -- basename of the client's uploaded file
  upload_ext  -- extension of the client's uploaded file
                 (extension also included in the basename)

This mixin makes use of undocumented properties of the FieldStorage
class in Python's cgi module.  It will be difficult to alter.
"""

import os,cgi

_error_msg = """ There is a problem with the upload mixin.  Has your tech guy been fooling with upload.py or support.js?  The problem is likely in one of those two places.  Or, maybe it lies in an upgrade to Python.
"""

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
    return data['upload--file-name']
  except:
    # get giveup and apply it
    (unmixed('out')).giveup( 
        'upload expander', 500, _error_msg
    )

def _upload_(cgi_obj,writefilename): 
  try:  
    with open(writefilename, 'wb') as fo:
       while True:
          chunk = cgi_obj.file.read(8192)
          if len(chunk) == 0:   break 
          else:                 fo.write(chunk)
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
<input type="file" id="upload--file-name"/> 
<button id='upload--submit'>submit upload</button>
"""


