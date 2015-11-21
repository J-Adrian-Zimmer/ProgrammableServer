'''
  This is the most complicated and least commented of 
  the demonstrations.  However the supporting 
  expander mixins `connect` and `upload` are well 
  commented.  
  
  Also use is made of two functions in js/support.js, 
  namely `file_out` and `get_css`.  These are 
  described in js/support.readme.
    
  BUT you should understand the echo demonstration 
  before working on this one.

  If more help is needed buy the ebooklet 
     
     "A Python Programmable Web Server" 
  
  by the author of this code.
'''

import os

## Note:  The id 'upload' is hardcoded here and in
## `upload.py`

## get() and post() ##   
    
def get():
  # invoked for get requests, rejects those which are 
  # not for uploadPic
  if request=='/uploadPic': 
     template = (unmixed('upload')).upload_template
     (unmixed('connect')).pageOut(
          title="Upload A Picture",
          other_head= loadCSS, 
          body= body % template
     )

def send(msg):
   template = (unmixed('upload')).upload_template

   # sends the message and raises Handled
   (unmixed('connect')).jsonOut( 
                { "response": msg,
                  "template":template }
                # template will need refreshing
   )

def post():
  # invoked for POST requests, rejects those which
  # are not for uploadPic
  if request=='/uploadPic':
    
    # extension check
    up = unmixed('upload') 
    if up.upload_ext.lower()!='jpg':
        send( "only accepting jpg files" )
   
   
    # copy uploaded file and respond 
    absfile = os.path.join( 
                (unmixed('localInfo')).web_root,
                'media',
                up.upload_filename
              )
    if up.upload(absfile):
       send( 'Upload OK.  Find picture at media/' 
               + up.upload_filename
            )
    send('Could not upload ' + os.path.normpath(absfile))

loadCSS = """
<script>

function $id(name) { return $('#'+name) }

function warn(clear){
   if(clear==='clear') {
      $id('storage-warning').html('')
   } else {
      $id('storage-warning').html(
         "local storage used to remember this layout"
      )
   }
}

function setDesktopCSS() {
   localStorage.setItem('mobile','no')
   warn()
   get_css('css/upload_desktop.css')
   console.log( 'THREE:' + localStorage.getItem('mobile') )
}
function setMobileCSS() {
   localStorage.setItem('mobile','yes')
   warn()
   get_css('css/upload_mobile.css')
   console.log( 'FOUR:' + localStorage.getItem('mobile') )
}

function tellResponse(jsn) {
   // a kludge to reset the selected file
   // (programmers aren't supposed to choose
   //  files so general method of setting
   //  the chosen file exists)
   $id('upload-chooser').html(jsn.template)
   // tell user what happened
   $id('response').html(jsn.response)
}

function submitClick() {
   // need to do this repeatedly because of
   // the kludge
   $id('upload--submit').click( function() {
      warn('clear')
      if( $id('upload--file-name')[0].value ) {
         file_out( 'uploadPic', tellResponse )
      }
   })
   warn('clear')
}

$(function() {
   if( localStorage.getItem('mobile')==='yes' ) {
      setMobileCSS()
   } else {
      setDesktopCSS()
   }
   submitClick();
   $id('desktop').click( setDesktopCSS );
   $id('mobile').click( setMobileCSS );
   $id('upload-chooser').click( function() {
         $id('response').html("");
         submitClick()
   })
})
</script>
"""
      
body = """
   <h1>Upload A Picture</h1>  
   <div id='info'>Source code for this demo is found in
      <code>demo_app\expanders\uploadPic</code>.
   </div>
   <div id='theform'>
     <p>This will upload a JPG picture to the media subdirectory.</p>
     <p id='upload-chooser'>%s</p>
     <p id='response'></p>
   </div>
   <div id='buttons'>
     <div><button id='desktop'>Choose Desktop Layout</div> 
     <div><button id='mobile'>Choose Mobile Layout</div>
     <p id='storage-warning'><p>
   </div>
""" 

