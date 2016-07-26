'use strict';

var fs = require( 'fs' ),
	path = require( 'path' ),
	express = require( 'express' ),
	app = express(),
	server = require( 'http' ).Server( app ),
	io = require( 'socket.io' )( server ),
	ft = require( 'file-tail' ),
	oDeviceIndex = {},
	oDevices, pathDevices, devId,
	exports = module.exports;

// Read the config file with all devices
pathDevices = path.resolve( __dirname, '..', '..', 'config', 'devices.json' );
oDevices = JSON.parse( fs.readFileSync( pathDevices ) );

// Generate an index for all devices for faster access later on
for( var el in oDevices ) {
	devId = oDevices[ el ].device;
	oDeviceIndex[ devId ] = el;
}

/*
 * Expects arguments:
 * filepath: the path to the file where you expect the z-way-log to be written to
 * port: the port on which to listen for clients to request the webpage or the socket events
 */
exports.startup = function( args ) {
	var eFT, watchingDeviceID,
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


	// We are looking for log entries like those below:

	// Switches
	// [2015-04-21 18:10:24.654] RECEIVED: ( 01 0D 00 04 00 0A 07 60 0D 01 01 20 01 FF 48 )
	// [2015-04-21 18:10:24.656] SENT ACK
	// [2015-04-21 18:10:24.657] SETDATA devices.10.data.lastReceived = 0 (0x00000000)
	// [2015-04-21 18:10:24.669] SETDATA devices.1.instances.1.commandClasses.32.data.srcNodeId = 10 (0x0000000a)
	// [2015-04-21 18:10:24.670] SETDATA devices.1.instances.1.commandClasses.32.data.srcInstanceId = 1 (0x00000001)
	// [2015-04-21 18:10:24.671] SETDATA devices.1.instances.1.commandClasses.32.data.level = 255 (0x000000ff)
		
	// Humidity and temperature
	// [2015-04-21 19:33:54.777] RECEIVED: ( 01 0B 00 04 00 05 05 31 05 03 01 0C CA )
	// [2015-04-21 19:33:54.778] SENT ACK
	// [2015-04-21 19:33:54.778] SETDATA devices.5.data.lastReceived = 0 (0x00000000)
	// [2015-04-21 19:33:54.783] SETDATA devices.5.instances.0.commandClasses.49.data.3.deviceScale = 0 (0x00000000)
	// [2015-04-21 19:33:54.784] SETDATA devices.5.instances.0.commandClasses.49.data.3.scale = 0 (0x00000000)
	// [2015-04-21 19:33:54.795] SETDATA devices.5.instances.0.commandClasses.49.data.3.val = 12.000000
	// [2015-04-21 19:33:54.889] SETDATA devices.5.instances.0.commandClasses.49.data.3.scaleString = "%"
	// [2015-04-21 19:33:54.890] SETDATA devices.5.instances.0.commandClasses.49.data.3 = Empty
	// [2015-04-21 19:33:54.910] RECEIVED: ( 01 0C 00 04 00 05 06 31 05 01 0A 00 49 82 )
	// [2015-04-21 19:33:54.912] SENT ACK
	// [2015-04-21 19:33:54.913] SETDATA devices.5.data.lastReceived = 0 (0x00000000)
	// [2015-04-21 19:33:54.914] SETDATA devices.5.instances.0.commandClasses.49.data.1.deviceScale = 1 (0x00000001)
	// [2015-04-21 19:33:54.931] SETDATA devices.5.instances.0.commandClasses.49.data.1.val = 22.799999
	// [2015-04-21 19:33:54.933] SETDATA devices.5.instances.0.commandClasses.49.data.1.scale = 0 (0x00000000)
	// [2015-04-21 19:33:54.948] SETDATA devices.5.instances.0.commandClasses.49.data.1.scaleString = "°C"
	// [2015-04-21 19:33:54.948] SETDATA devices.5.instances.0.commandClasses.49.data.1 = Empty

	// Let's see if we find a device function that matches the current log entry as displayed above
	function getKnownDeviceAndFunction( devId, arrProps ) {
		if( devId < 0 ) return null;
		var func,
			devName = oDeviceIndex[ devId ],
			oDev = oDevices[ devName ];

		for( var el in oDev.functions ) {
			func = oDev.functions[ el ];
			if( parseInt(arrProps[ 3 ]) === func.instance
					&& parseInt(arrProps[ 5 ]) === func.commandClass ) {
				if( typeof( func.data ) === 'string' ) {
					if( arrProps[ 7 ] === func.data ) {
						return {
							functionName: el,
							deviceName: devName,
							device: oDev
						};
					}
				} else {
					if( arrProps[ 7 ] === func.data.key
							&& arrProps[ 8 ] === func.data.val ) {
						return {
							functionName: el,
							deviceName: devName,
							device: oDev
						};
					}
				}
			}
		}
	}

	watchingDeviceID = -1;
	eFT.on( 'line', function( line ) {
		var arrKeyVal, arrProps, oEvent, oDat,
			i = line.indexOf( 'SETDATA' );
		if( i > -1 ) {
			console.log( 'Found in Log: ' + line );

			// A SETDATA log entry always has an equal sign...
			arrKeyVal = line.substring( i + 8 ).split( ' = ' );

			// ... hence before the equal sign we find the key
			arrProps = arrKeyVal[ 0 ].split( '.' );

			// Try to find a function in the watched device to know whether we want to send this as an event
			if( (oEvent = getKnownDeviceAndFunction(watchingDeviceID, arrProps)) ) {
				oDat = oDataStore[ oEvent.deviceName ];
				if( !oDat ) {
					oDat = oDataStore[ oEvent.deviceName ] = {};
				}
				if( oDat[ oEvent.functionName ] !== arrKeyVal[ 1 ] ) {
					console.log( 'Emitting event: Delta in "%s": "%s" !== "%s"', oEvent.deviceName, oDat[ oEvent.functionName ], arrKeyVal[ 1 ] );
					oEvent.data = oDat[ oEvent.functionName ] = arrKeyVal[ 1 ];
					oEvent.detected = new Date;
					io.emit( 'state', oEvent );
					watchingDeviceID = -1;
				}
			}
		
			// Let's check whether this is the initialization line for new data
			if( watchingDeviceID < 0
					&& arrProps[ 0 ] === 'devices'
					// check wehther this is a device we are looking for:
					&& oDeviceIndex[ arrProps[ 1 ] ]
					&& arrProps[ 2 ] === 'data'
					&& arrProps[ 3 ] === 'lastReceived' ) {
				// NICE! We are receiving a new event! Let's look at the other lines showing up soon!
				watchingDeviceID = arrProps[ 1 ];
			}
		}
	});

}