# This code and that in echoHandler.py demonstrate 
# how objects can be sent to the server and back.
# When the buttons are clicked, an object with the
# textarea text and a goal ('uppercase' or 'lowercase')
# is sent to this way.  The server runs echoHandler
# to convert the text and send it back to this 
# echo page.

# The get function serves up the echo page.

def get():
  using('jsonSupport')  
  #     jsonSuppor is a mixin found in the server's
  #     expander_mixin directory
  #     it supplies ajaxable_page which creates a paage
  #     with jQuery and the necessary javascxript to run
  #     jQuery's ajax handler
  if request=='/echo':
     ajaxable_page(
         title = 'JSON Example for ProgrammableRequestHandler',
         cssList = _css,
         other_part = _other_part,  # inline Javascript
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

_css = ["css/echo.css"]

_other_part = """
<script>
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
