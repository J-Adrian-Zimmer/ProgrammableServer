import os

## helper functions ##

def _ip_ok(handler):
    # reject ip if not local
    # this will not work if there is a proxy server
    # because the proxy is seen as local
    ip = handler.client_address[0]
    return ip[:7]=='192.168' or ip[:9]=='127.0.0.1'

def _send_html(message):
  using('upload','out')
  #      upload and out are mixins found in the server's
  #      expander_mixin subdirectory
  #      upload provides upload_template
  #      out provides page_out
  form_template = upload_template % ('pic_form','uploadPic')
  page_out(
       title="Upload A Picture",
       body= body % (form_template,message)
  )
def _defang_name(name):
  from re import sub
  return sub(unwanted_chars,'',name)

## get() and post() ##   
    
def get():
  # invoked for get requests, rejects those which are 
  # not for uploadPic

  if request=='/uploadPic': _send_html('')

def post():
  # invoked for POST requests, rejects those which
  # are not for uploadPic

  using('upload','config')
  #     upload is a mixin found in the server's
  #     expander_mixin subdirectory; it provides
  #     upload and upload_ext

  if request=='/uploadPic':

    # possible errors
    if not _ip_ok(handler):
       _send_html(
         "Only accepting requests from local network."
       )
    if upload_ext.lower()!='jpg':
        _send_html( "only accepting jpg files" )
    
    # upload it
    absfile = os.path.join( 
                web_root,
                'media',
                _defang_name(upload_filename)
              )
    if upload(absfile):
       _send_html(
          'Upload OK.  Find picture at ' + absfile 
       )
    else:
       _send_html(
         'Could not upload '+_defang_name(upload_filename)
       )

body = """
   <h1>Upload A Picture</h1>  
   <p>Source code for this app is found in
   <code>demo_app\expanders\uploadPic</code>.
   </p>
   <div>%s</div>
   <p>This will upload a JPG picture to the media subdirectory, 
   provided you are working from a local network.</p>
   <p>%s</p>
""" 

