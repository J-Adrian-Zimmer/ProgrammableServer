function fixWhiteSpace(txt) {
   return txt.replace(/\s+/,' ')
}

function json_out( 
       app, // the app doing the sending
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
          var obj = JSON.parse(
                    fixWhiteSpace(data.responseText) );
          $('body').html(obj.body);
          $('head').append(obj.css);
          $('head > title').replaceWith(obj.title);
          $('body').html(obj.body);
     })

} // no return value, no wait
