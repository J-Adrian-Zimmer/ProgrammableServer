'''
  The uploadPic expander uses an HTML form to upload 
  a picture to web_root/media.  The picture must be
  a jpg and the browser must be on the same computer
  as the server
'''

import os

## helper functions ##

def _send_html(message):
  up = unmixed('upload')
  out = unmixed('out')
       # like using( 'upload','out' ) but makes the up and
       # out variables reference the expander_mixins 
       # rather than mixing it into the local namespace
  form_template = up.upload_template % ('pic_form','uploadPic')
  out.page_out(
       title="Upload A Picture",
       body= body % (form_template,message)
  )

## get() and post() ##   
    
def get():
  # invoked for get requests, rejects those which are 
  # not for uploadPic
  if request=='/uploadPic': _send_html('')

def post():
  # invoked for POST requests, rejects those which
  # are not for uploadPic
  if request=='/uploadPic':
    mixins('upload')  # for upload_template, upload_ext 
                      # upload_filename, and upload
    me = unmixed('network').me
    web_root = unmixed('constants').web_root

    if not me():
       _send_html(
         "Only accepting requests from same computer."
       )
    if upload_ext.lower()!='jpg':
        _send_html( "only accepting jpg files" )
    
    # upload it
    absfile = os.path.join( web_root,'media',upload_filename )
    if upload(absfile):
       _send_html(
          'Upload OK.  Find picture at media/' + upload_filename
       )
    else:
       _send_html(
         'Could not upload '+ 
         os.path.normpath(absfile)
       )

body = """
   <h1>Upload A Picture</h1>  
   <p>Source code for this demo is found in
   <code>demo_app\expanders\uploadPic</code>.
   </p>
   <div>%s</div>
   <p>This will upload a JPG picture to the media subdirectory, 
   provided you are working from a local network.</p>
   <p>%s</p>
""" 

