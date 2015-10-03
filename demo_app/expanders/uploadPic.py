import os

## helper functions ##

def _ip_ok(handler):
    # reject ip if not local
    # this will not work if there is a proxy server
    # because the proxy is seen as local
    ip = handler.client_address[0]
    return ip[:7]=='192.168' or ip[:9]=='127.0.0.1'

def _send_html(message):
  print 'UPLOADPIC _send_html'
  using('upload','out')
  form_template = upload_template % ('pic_form','uploadPic')
  page_out(
       title="Upload A Picture",
       js = js,
       css=css,
       body= body % (form_template,message)
  )
def _defang_name(name):
  from re import sub
  from config import unwanted_chars
  return sub(unwanted_chars,'',name)

## get() and post() ##   
    
def get():
  handler.server.soconsts.dbg('uploadPic GET')
  if request=='/uploadPic': _send_html('')

def post():
  handler.server.soconsts.dbg('uploadPic POST')
  using('upload','details')
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

css = """
"""

js = """
"""

body = """
   <h1>Upload A Picture</h1>  <button>Day/Night</button>
   <div>%s</div>
   <p>This will upload a JPG picture to the media subdirectory, 
   provided you are working from a local network.</p>
   <p>%s</p>
""" 

