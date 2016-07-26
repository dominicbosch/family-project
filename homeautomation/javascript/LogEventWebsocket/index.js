'use strict';

var fs = require( 'fs' ),
	path = require( 'path' ),
	express = require( 'express' ),
	app = express(),
	server = require( 'http' ).Server( app ),
	io = require( 'socket.io' )( server ),
	ft = require( 'file-tail' ),
	oDeviceIndex = {},
	oDevices, pathDevices, devId;

// Read the config file with all devices
pathDevices = path.resolve( __dirname, '..', '..', 'config', 'devices.json' );
oDevices = JSON.parse( fs.readFileSync( pathDevices ) );

// Generate an index for all devices for faster access later on
for( var el in oDevices ) {
	devId = oDevices[ el ].device;
	oDeviceIndex[ devId ] = el;
}

// Checks whether the pproperties define a device we are looking for
// We want to see a line like this in the log file:
// [2015-02-14 14:27:43.964] SETDATA devices.8.instances.0.commandClasses.49.data.5.val = 65.000000
function getWantedDevice( arrProperties ) {
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
}

var exports = module.exports;

exports.startup = function( args ) {
	// filepath = path.resolve( __dirname, '..', '..', '..', 'logs', 'z-way-server.log' ),
	var eFT,
		filepath = args.filepath || '/var/log/z-way-server.log',
		oListeners = {},
		oDataStore = {},
		idxListener = 1,
		port = parseInt( args.port ) || 4321;

	// Starting to listen for clients on port
	server.listen( port );
	console.log( 'Starting to listen on port ' + port );

	// We serve static web content from the webserver folder
	app.use( express.static( __dirname + '/webserver' ) );

	// A new client connected through a WebSocket
	io.on( 'connection', function ( socket ) {
		// We give all the clients an incremental ID
		var id = 'listener_' + idxListener++;

		// We store the socket in an interal list
		oListeners[ id ] = socket;
		console.log( 'new socket connected from ' + socket.conn.remoteAddress );

		// We purge the socket from the list because it's gone
		socket.on( 'disconnect', function () {
			delete oListeners[ id ];
		});
	});

	// Start to listen for events in the log file
	eFT = ft.startTailing( filepath );

	// [2015-04-21 18:10:24.654] RECEIVED: ( 01 0D 00 04 00 0A 07 60 0D 01 01 20 01 FF 48 )
	// [2015-04-21 18:10:24.656] SENT ACK
	// [2015-04-21 18:10:24.657] SETDATA devices.10.data.lastReceived = 0 (0x00000000)
	// [2015-04-21 18:10:24.669] SETDATA devices.1.instances.1.commandClasses.32.data.srcNodeId = 10 (0x0000000a)
	// [2015-04-21 18:10:24.670] SETDATA devices.1.instances.1.commandClasses.32.data.srcInstanceId = 1 (0x00000001)
	// [2015-04-21 18:10:24.671] SETDATA devices.1.instances.1.commandClasses.32.data.level = 255 (0x000000ff)

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
					console.log( 'Emitting event: Delta in "%s": "%s" !== "%s"', oDevice.deviceName, oDat[ oDevice.functionName ], arrKeyVal[ 1 ] );
					oDevice.data = oDat[ oDevice.functionName ] = arrKeyVal[ 1 ];
					oDevice.detected = new Date;
					io.emit( 'state', oDevice );
				}
			}
		}
	});

}