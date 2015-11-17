// supports the toggle expander only
//
// that expander demonstrates the use of set_web_root
// and is not included in expanderOrderings.editable
// because its value is dubious

function queryStatus() {
   // the first action must be to find out 
   // current web_root status
   json_out(
      'toggle',
      { cmd: 'query' },
      initialize
   )
}

function initialize(jsn) {
   // initialize after we know if web_root
   // is server_dir or not
   if( jsn.result=='server dir' ) {
      setToDemo()
   } else {
      setToServer()
   }
}

function setToServer() {
// setup for a button that switches web_root to server_dir
$('h2').html(
"Click for files from <button id='butt'>server's</button> public directory."
)
setTimeout(
   // hesitate so html is changed before we assign 
   // a handler to the button 
   function() {
      $('#butt').click(toServer)
   },
   250
)
}

function setToDemo() {
// setup for a button that switches web_root to demo_app dir
$('h2').html(
"Click for files from <button id='butt'>demonstrations's</button> public directory."
)
setTimeout(
   // hesitate so html is changed before we assign 
   // a handler to the button 
   function() {
      $('#butt').click(toDemo)
   },
   250
)
}

function toDemo() {
// switch to demo_app dir and setup for switching back
   $('h2').html("Requesting change to demo's public dir ...")
   json_out(
      'toggle',
      { cmd:'to demo' },
      setToServer
   )
}

function toServer() {
// switch to server_dir and setup for switching back
   $('h2').html("Requesting change to server's public dir ...")
   json_out(
      'toggle',
      { cmd:'to server' },
      setToDemo
   )
}
      

