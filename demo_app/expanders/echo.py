'''
This code and that in echoHandler.py demonstrate how
objects can be sent to the server and back.

When the buttons are clicked, an object with the
textarea text and a goal ('uppercase' or 'lowercase')
is sent to the server.

This is possible because the spage_out method formats
a page which loads a support.js file.  This Javascript
file has a method json_out that sends a string formated
as a JSON object to the server using jQuery's support for
Ajax transfers.

Most of spage_out's behavior comes from the page_out
function in the out mixin.
'''

def get():
  if request=='/echo':
     mixins('jsonConnect')  # for spage_out
          # jsonConnect.py is found in expander_mixins
     spage_out(
         title = 'Asynchronous Javascript & JSON Example',
         cssList = _css,
         other_head = _javascript,  
                      # happens to be inline Javascript
         body = body
     )

body = """
<h2>Enter Text & Choose Upper or Lower Case</h2>
<p>
Source code for this demo is at
<code>demo_app/expanders/echo.py</code> and
<code>demo_app/expanders/echoHandler.py</code>.
</p><p>
This page is a demonstration of how the Programmable Server
handles AJAX communication of JSON objects.  That is why its
simple functionality is implemented in the server using Python 
rather than in the browser using Javascript.  
</p>

<div id='left'>
<textarea id='echome'></textarea>
<div id='controls'>
<button id='upper'>All Uppercase</button>
<button id='lower'>All Lowercase</button>
</div>
</div><div id='right'>
<textarea id='echoarea'></textarea>
</div>

""" 

_css = ["echo.css"]

_javascript = """
<script> 

/* 
this script could have been loaded from a file with
spage_out's jsList parameter.   Merely showing
another possibility here.   jQuery is loaded automatically
by both page_out and spage_out.  See the config.py file.
*/

function $id(x) {
   return $('#'+x)
}

function writeEchoArea(jsn) {
   // callback for the json ajax request
   $id('echoarea').val(jsn.text)
}

$( function() {  // bind the handler when page loaded

   $id('upper').click( function() {
      var txt = $id('echome').val();
      json_out( 'echoHandler', 
                { text: txt, goal: 'uppercase' }, 
                writeEchoArea
      )
   } )
   
   $id('lower').click( function() {
      var txt = $id('echome').val();
      json_out( 'echoHandler', 
                { text: txt, goal: 'lowercase' }, 
                writeEchoArea
      )
   } )

   $id('echoarea').keypress( function(event) {
      // disable the area without showing any sign of it
      event.preventDefault()
   } )

} )
</script>
"""
