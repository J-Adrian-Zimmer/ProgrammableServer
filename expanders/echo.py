# This code and that in echoHandler.py demonstrate 
# how objects can be sent to the server and back.
# When the buttons are clicked, an object with the
# textarea text and a goal ('uppercase' or 'lowercase')
# is sent to this way.  The server runs echoHandler
# to convert the text and send it back to this 
# echo page.

# The get function serves up the echo page.
# It gets pathpargs from parsepath and page_out
# from jsonSupport -- page_out puts out a page
# with a javascript function send_json which
# is invoked when the buttons are clicked


def get():
  using('basic','jsonSupport')  
  if path=='/echo':
     page_out(
         title = 'JSON Example for ProgrammableRequestHandler',
         js = js,
         css = css,
         body = body
     )


body = """
<h4>Enter Text & Play</h4>
<p>
This page is a demonstration of how ProgrammableServer
handles Ajax communication of JSON objects.  That is why its
simple functionality is implemented in the server using Python 
rather than in the browser using Javascript.  
</p><p>
If you lookup the code in these short files, you will
see how this application is implemented.
</p>
<ul>
<li>config.py</li>
<li>expanders/echo.py</li>
<li>expanders/echoHandler.py</li>
<li>expanders/shutdown.py</li> 
</ul>
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

css = """
<link rel="stylesheet" type="text/css" href="css/echo.css"/>
"""

js = """
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
