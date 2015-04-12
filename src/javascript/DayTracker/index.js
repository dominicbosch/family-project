var url, socket, fs = require( 'fs' ),
	ioclient = require( 'socket.io-client' );

url = 'http://192.168.0.79:4321';
socket = ioclient( url );

socket.on( 'connect', function() { console.log( 'Connected to ' + url ); });
socket.on( 'disconnect', function() { console.log( 'Disconnectedl from ' + ur ); });

socket.on( 'state', function( data ) {
	data.received = new Date;
	fs.appendFile('message.txt', JSON.stringify( data ) + '\n' );
});




