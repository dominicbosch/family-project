var request = require( 'request' ),
    payload = {
      test: 'property',
      message: 'wow',
      nested: {
        test: 'property',
        message: 'wow',
        nested: {
          test: 'property',
          message: 'wow',
          nested: {
            test: 'property',
            message: 'wow'
          }
        }
      }
    };

request({
  url: 'http://localhost:8888/eventlistener',
  method: 'POST',
  json: payload,
  success: function( response ) {
    console.log( 'Successfully forwarded event:' );
    console.log( JSON.stringify( payload ) );
  },
  error: function( response ) {
    console.log( 'Error during forwarding request: ' + response.statusText );
  } 
}); 