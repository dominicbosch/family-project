var express = require( 'express' ),
	bodyParser = require( 'body-parser' ),
	app = express();

// app.use( bodyParser.json() );

// http%3A%2F%2F192.168.0.43%3A8234%2Fevent
app.post( '/event', bodyParser.json(), function( req, res ) {
	console.log( 'got event: ', JSON.stringify(req.body));
});

app.listen( 8234 );

console.log( 'Listening for events on 8234' );