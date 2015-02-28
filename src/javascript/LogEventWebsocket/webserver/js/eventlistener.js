
$( document ).ready( function() {
	console.log( 'trying to connect!');
		// we read the port of the current website
	var port = (location.port === '') ? '' : ':' + location.port,
		// we create a connection to the websocket server on exactly this port
		socket = io( port + '/' ),
		// we grab the element on the current website where we will put the event information
		eventEl = $( 'h1' );


	// As soon as we are connected we could handle it with this below:
	socket.on( 'connect', function() {
		eventEl.after( $( '<div>' ).addClass( 'success' ).text( 'WebSocket connected!' ) );
	});
	
	// Somehow we got disconnected from the socket... dammit!
	socket.on( 'disconnect', function() {
		eventEl.after( $( '<div>' ).addClass( 'error' ).text( 'WebSocket disconnected!' ) );
	});
	
	// We got a new state event from the websocket provider:
	socket.on( 'state', function( data ) {
		console.log( data );
		var str = data.deviceName + '(' + data.functionName + '): ' + data.data;
		eventEl.after( $( '<div>' ).addClass( 'info' ).text( str ) );
	});
});