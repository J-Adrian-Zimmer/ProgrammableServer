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
       # like mixins( 'upload','out' ) but makes the up and
       # out variables reference the expander_mixins 
       # rather than mixing it into the local namespace
  form_template = up.upload_template % ('pic_form','uploadPic')
  out.page_out(
       title="Upload A Picture",
       jsList= ['support.js'],
       other_head= loadCSS, 
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
    up = unmixed('upload') 
    elsewhere = unmixed('requestInfo').client_ip!='127.0.0.1'
    web_root = unmixed('localInfo').web_root
    if elsewhere:
       _send_html(
         "Only accepting requests from same computer."
       )
    if up.upload_ext.lower()!='jpg':
        _send_html( "only accepting jpg files" )
    # upload it
    absfile = os.path.join( 
                web_root,
                'media',
                up.upload_filename
              )
    if up.upload(absfile):
       _send_html(
          'Upload OK.  Find picture at media/' + up.upload_filename
       )
    else:
       _send_html(
         'Could not upload '+ 
         os.path.normpath(absfile)
       )

loadCSS = """
<script>
function $id(name) { return $('#'+name) }
function setDesktopCSS() {
   get_css('css/upload_desktop.css')
}
function setMobileCSS() {
   get_css('css/upload_mobile.css')
}

$(function() {
   setDesktopCSS()
   $id('desktop').click( setDesktopCSS );
   $id('mobile').click( setMobileCSS );
})
</script>
"""
      
body = """
   <h1>Upload A Picture</h1>  
   <div id='info'>Source code for this demo is found in
      <code>demo_app\expanders\uploadPic</code>.
   </div>
   <div id='theform'>
     <p>This will upload a JPG picture to the media subdirectory, 
     provided you are working from a local network.</p>
     <p>%s</p>
     <p>%s</p>
     <p>
     The <code>Choose</code> buttons demonstrate a feature that helps creating
     responsive web pages.  Each button loads a CSS file 
     and applies it.
     </p>
   </div>
   <div id='buttons'>
     <div><button id='desktop'>Choose Desktop Layout</div> 
     <div><button id='mobile'>Choose Mobile Layout</div>
     <p>
     See <code>/py/css_parse.py</code> for restrictions on 
     the CSS which can be used.
     </p>
   </div>
""" 

