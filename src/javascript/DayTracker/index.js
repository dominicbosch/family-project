var fs = require( 'fs' ),
	ioclient = require( 'socket.io-client' ),
	socket = ioclient( 'http://192.168.0.79:4321' );

socket.on( 'connect', function() { console.log( 'connected' ); });

socket.on( 'state', function( data ) {
	if( data.device.type === 'switch' ) {
		var str = '[' + (new Date).toLocaleString() + '] ' + JSON.stringify( data );
		console.log( 'Appending event: ' + str );
		fs.appendFile('message.txt', str + '\n' );
	}
});

socket.on( 'disconnect', function() { console.log( 'disconnected' ); });


