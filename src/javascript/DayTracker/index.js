var url, socket, fs = require( 'fs' ),
	ioclient = require( 'socket.io-client' ),
	exports = module.exports;

/*
 * Expects arguments:
 * logPath: the path to where the event log should be written to
 * url: the url where we want to register to a web socket
 */
exports.startup = function( args ) {
	var url = args.url || 'http://192.168.0.79:4321',
		logPath = args.logPath || 'daytracker.log';

	console.log( 'DayTracker starting up, trying to connect to "' + url 
		+ '" and I will store detected events to "' + logPath + '"');

	ioclient( url )
		.on( 'connect', function() { console.log( 'Connected to ' + url ); })
		.on( 'disconnect', function() { console.log( 'Disconnected from ' + url ); })
		.on( 'state', function( data ) {
			data.received = new Date;
			fs.appendFile('message.txt', JSON.stringify( data ) + '\n' );
		});
}

