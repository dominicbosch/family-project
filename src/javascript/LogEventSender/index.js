'use strict';

var eFT, pathDevices, getWantedDevice, oDeviceIndex, devId,
	oDevices, arrListenerURLs, sendEvent,
	fs = require( 'fs' ),
	path = require( 'path' ),
	ft = require( 'file-tail' ),
	express = require( 'express' ),
	app = express(),
	filename = '/var/log/z-way-server.log';

// Read the config file with all devices
pathDevices = path.resolve( __dirname, '..', '..', 'config', 'devices' );
oDevices = JSON.parse( fs.readFileSync( pathDevices ) );

// Generate an index for all devices for faster access later on
for( var el in oDevices ) {
	devId = oDevices[ el ].device;
	oDeviceIndex[ devId ] = el;
}

getWantedDevice = function( arrProperties ) {

};
// We want to see a line like this in the log file:
// [2015-02-14 14:27:43.964] SETDATA devices.8.instances.0.commandClasses.49.data.5.val = 65.000000
eFT.on( 'line', function( line ) {
	var i = line.indexOf( 'SETDATA' );
	if( i > -1 ) {

	// var arrProps = line.split( '.' );

	// if( isWant)
	// for ( var i = 0; i < arrListenerURLs.length; i++ ) {
	// 	arrListenerURLs[ i ]
	// }
    console.log(line);
	}
});

app.get( '/register/:url', function( req, res ) {
	var url = req.params.url;
	// Add the url only if it wasn't already registered
	if( arrListenerURLs.indexOf( url ) < 0 ) arrListenerURLs.push( url );
});

app.get( '/unregister/:url', function( req, res ) {
	var id, url = req.params.url;
	// Remove the URL from the array if it's existing in the array
	id = arrListenerURLs.indexOf( url );
	if( id > -1 ) arrListenerURLs.splice( id, 1 );
});

// Start to listen for new URL registrations on port 8123
app.listen( 8123 );

// Start to listen for events in the log file
eFT = ft.startTailing( filename );
