'use strict';

var eFT, pathDevices, getWantedDevice, devId,
	oDevices, arrListenerURLs = [],
	oDeviceIndex = {},
	fs = require( 'fs' ),
	path = require( 'path' ),
	needle = require( 'needle' ),
	ft = require( 'file-tail' ),
	express = require( 'express' ),
	app = express(),
	// filename = path.resolve( __dirname, '..', '..', '..', 'logs', 'z-way-server.log' );
	filename = '/var/log/z-way-server.log';

// Read the config file with all devices
pathDevices = path.resolve( __dirname, '..', '..', 'config', 'devices.json' );
oDevices = JSON.parse( fs.readFileSync( pathDevices ) );

// Generate an index for all devices for faster access later on
for( var el in oDevices ) {
	devId = oDevices[ el ].device;
	oDeviceIndex[ devId ] = el;
}

app.get( '/register/:url', function( req, res ) {
	var url = req.params.url;
	// Add the url only if it wasn't already registered
	if( arrListenerURLs.indexOf( url ) < 0 ) {
		arrListenerURLs.push( url );
		console.log( 'New event listener registered: ', url );
		res.send( 'Thank you for registering "' + url + '" for events! Enjoy!');
	} else  res.send( 'Already registered: ' + url );
});

app.get( '/unregister/:url', function( req, res ) {
	var id, url = req.params.url;
	// Remove the URL from the array if it's existing in the array
	id = arrListenerURLs.indexOf( url );
	if( id > -1 ) {
		arrListenerURLs.splice( id, 1 );
		console.log( 'Event listener removed: ', url );
		res.send( 'You unregistered "' + url + '" for events! :\'-(');
	} else res.send( 'Not existing: ' + url );
});

// Start to listen for events in the log file
eFT = ft.startTailing( filename );

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

// We want to see a line like this in the log file:
// [2015-02-14 14:27:43.964] SETDATA devices.8.instances.0.commandClasses.49.data.5.val = 65.000000
eFT.on( 'line', function( line ) {
	var arrKeyVal, arrVals, arrProps, oDevice,
		i = line.indexOf( 'SETDATA' );
	if( i > -1 ) {
		console.log( 'New SETDATA line: ' + line );

		// A SETDATA log entry always has an equal sign...
		arrKeyVal = line.substring( i + 8 ).split( ' = ' );
		// ... hence before the equal sign we find the key and ...
		arrProps = arrKeyVal[ 0 ].split( '.' );
		// ... after the equal sign we find the value (sometimes in two representations such as also HEX)
		
		if( arrKeyVal[ 1 ] ) {
			arrVals = arrKeyVal[ 1 ].split( ' ' );

			oDevice = getWantedDevice( arrProps );
			if( oDevice ) {
				oDevice.data = arrVals;
				for( var i = 0; i < arrListenerURLs.length; i++ ) {
					needle.request( 'post', arrListenerURLs[ i ], oDevice, { json: true }, function( err, resp ) {
						if( resp ) console.log( resp.body );
					});
				}
			}
		}
	}
});

// Start to listen for new URL registrations on port 8123
app.listen( 8123 );

console.log( 'Running on port 8123 and listening to file changes...');