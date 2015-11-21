// see support.readme

function fixWhiteSpace(txt) {
   return txt.replace(/\s+/,' ')
}

function alter_css(css_obj) {
   function apply_css( selector, obj ) {
      changes = {}
      $.each(
         obj, 
         function(property, value ) {
            changes[ property ] =  value 
         }
      )
      $(selector).css(changes)
   }

   $.each( css_obj, apply_css )
}

function get_css(filename) {
   json_out( 
       'css_response',
       { css_path_name: filename },
       alter_css
   )
}

function json_out( app, obj, cb) {

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

} 

function file_out( app, cb ) {
   var form = $('#upload--file-name')[0],  // want dom object
       file = form.files[0],
       sendable_form = new FormData(),
       xhr = new XMLHttpRequest();
   sendable_form.append('upload--file-name',file)
   $.ajax(
       { type:'POST',
         url:app,
         contentType:false,
         enctype:'multipart/form-data',
         processData: false,
         data: sendable_form
   }).done( function(data) {
       cb( JSON.parse(data) )
   }).fail( function(data) {
       $('body').html(data.responseText)
   })
}
