var express = require( 'express' ),
    app = express();

app.post( '/eventlistener', function( req, res ) {
  var body = '';

  req.on( 'data', function( chunk ){ body += chunk; });

  req.on( 'end', function(){
    console.log( 'Got event: ', JSON.parse( body ) );
    res.send( 'Thank you!' );
  });
});

app.listen( 8888 );
console.log( 'listening for events on port 8888' );