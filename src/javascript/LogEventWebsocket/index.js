'use strict';

var fs = require( 'fs' ),
	path = require( 'path' ),
	express = require( 'express' ),
	app = express(),
	server = require( 'http' ).Server( app ),
	io = require( 'socket.io' )( server ),
	ft = require( 'file-tail' ),
	// filename = path.resolve( __dirname, '..', '..', '..', 'logs', 'z-way-server.log' ),
	filename = '/var/log/z-way-server.log',
	oListeners = {},
	oDeviceIndex = {},
	oDataStore = {},
	idxListener = 1,
	oDevices, eFT, pathDevices,
	getWantedDevice, devId, io;

// Starting to listen for clients on port 4321
server.listen( 4321 );

// We serve static web content from the webserver folder
app.use( express.static( __dirname + '/webserver' ) );

// A new client connected through a WebSocket
io.on( 'connection', function ( socket ) {
	// We give all the clients an incremental ID
	var id = 'listener_' + idxListener++;

	// We store the socket in an interal list
	oListeners[ id ] = socket;
	console.log( 'new socket connected from ' + socket.conn.remoteAddress );

	socket.emit( 'event', { hello: 'world' });
	socket.on('my other event', function (data) {
		console.log(data);
	});

	// We purge the socket from the list because it's gone
	socket.on( 'disconnect', function () {
		delete oListeners[ id ];
	});
});

// Read the config file with all devices
pathDevices = path.resolve( __dirname, '..', '..', 'config', 'devices.json' );
oDevices = JSON.parse( fs.readFileSync( pathDevices ) );

// Generate an index for all devices for faster access later on
for( var el in oDevices ) {
	devId = oDevices[ el ].device;
	oDeviceIndex[ devId ] = el;
}

getWantedDevice = function( arrProperties ) {
	var cmd, oFuncs, id = oDeviceIndex[ arrProperties[ 1 ] ];
	if( id ) {
		oFuncs = oDevices[ id ].functions;
		for( var func in oFuncs ) {
			cmd = oFuncs[ func ].command.replace( /\[/g, '.' ).replace( /\]/g, '' );
			if( oFuncs[ func ].instance === parseInt(arrProperties[ 3 ])
					&&  oFuncs[ func ].commandClass === parseInt(arrProperties[ 5 ])
					&&  cmd === arrProperties.slice( 6 ).join( '.' ) ) {
				return {
					functionName: func,
					deviceName: id,
					device: oDevices[ id ]
				};
			}
		}
	}
};

// Start to listen for events in the log file
eFT = ft.startTailing( filename );

// We want to see a line like this in the log file:
// [2015-02-14 14:27:43.964] SETDATA devices.8.instances.0.commandClasses.49.data.5.val = 65.000000
eFT.on( 'line', function( line ) {
	var arrKeyVal, arrVals, arrProps, oDevice, oDat,
		i = line.indexOf( 'SETDATA' );
	if( i > -1 ) {
		console.log( 'Found in Log: ' + line );

		// A SETDATA log entry always has an equal sign...
		arrKeyVal = line.substring( i + 8 ).split( ' = ' );

		// ... hence before the equal sign we find the key and ...
		arrProps = arrKeyVal[ 0 ].split( '.' );

		// ... after the equal sign we find the value (sometimes in two representations such as also HEX)
		oDevice = getWantedDevice( arrProps );
		if( oDevice ) {
			oDat = oDataStore[ oDevice.deviceName ];
			if( !oDat ) {
				oDat = oDataStore[ oDevice.deviceName ] = {};
			}
			if( oDat[ oDevice.functionName ] !== arrKeyVal[ 1 ] ) {
				oDevice.data = oDat[ oDevice.functionName ] = arrKeyVal[ 1 ];
				console.log( 'Emitting event: Delta in "%s": "%s" !== "%s"', oDevice.deviceName, oDat[ oDevice.functionName ], arrKeyVal[ 1 ] );
				io.emit( 'state', oDevice );
			}
		}
	}
});

// Start to listen for new URL registrations on port 8123
// app.listen( 8123, function() {
// 	console.log( 'Running on port 8123 and listening to file changes...');
// });
