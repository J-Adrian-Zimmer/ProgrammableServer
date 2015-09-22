function black() {
   $('body').css( { color:'white', backgroundColor:'black' } )
   $('button').click( white )
}

function white() {
   $('body').css( { color:'black', backgroundColor:'white' } )
   $('button').click( black )
}

$( function() { $('button').click( black ) } )


