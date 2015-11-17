function fixWhiteSpace(txt) {
   return txt.replace(/\s+/,' ')
}

function alter_css(css_obj) {
   function apply_css( selector, obj ) {
      changes = {}
      $.each(
         obj, 
         function(property, value ) {
            console.log( '!!! ' + property + ',' + value + ' !!!')
            changes[ property ] =  value 
         }
      )
      $(selector).css(changes)
   }

   $.each( css_obj, apply_css )
}

function get_css(filename) {
   console.log('!!! get_css:' + filename + ": !!!")
   json_out( 
       'css_response',
       { css_path_name: filename },
       alter_css
   )
}

function json_out( 
   app, // responding url
   obj, // obj is javascript object without methods
   cb   // callback is invoked this way
        //    cb( obj )
        // obj is a json object from server
){

 $.ajax(
     { type:'POST',
       url:app,
       contentType:'text/plain',
       data: JSON.stringify(obj)
     }).done( function(data) {
          cb( JSON.parse(data) )
     }).fail( function(data) {
          $('body').html(data.responseText)
     })

} // no return value, no wait
