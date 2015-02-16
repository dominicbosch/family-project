'use strict';

var getPID, pid, killProc, child, startApp,
	fs = require( 'fs' ),
	path = require( 'path' ),
	proc = require( 'child_process' ),
	appName = process.argv[ 2 ],
	pidfile = path.resolve( __dirname, 'pids', appName + '.pid' ),
	logfile = path.resolve( __dirname, 'logs', appName + '.log' );

if( !process.argv[ 2 ] || process.argv[ 2 ] === 'help' ) {
	console.log( '\n\nUSAGE: "nodejs service [servicename] start|stop|restart"\n\n' 
		+ '\tWhere [servicename] means that this service handler will look for\n' 
		+ '\ta index.js file in a folder named [servicename] in this directory\n' 
		+ '\tand tries to run it with the provided command argument!\n');
	return;
}

killProc = function( pid ) {
	try {
		process.kill( pid );
		console.log( 'Process #' + pid + ' killed' );
	} catch( e ) {
		console.log( 'Process not killed?' );
	}
	fs.unlink( pidfile, function( err ) {
		if( err ) console.log( 'Unable to delete pid file, maybe it wasn\'t existing' );
	});
};

startApp = function() {
	var options;

	// First we kill the old log file
	fs.unlink( logfile, function( err ) {
		if( err ) console.log( 'Unable to delete log file, maybe it wasn\'t existing' );
	});
	// Then we open new stdout and stderr streams for the log file
	options = {
		detached: true,
		stdio: [
			'ignore',
			fs.openSync( logfile, 'a' ), // STDOUT
			fs.openSync( logfile, 'a' )  // STDERR
		]
	};
	// Finally we spawn a new child process ...
	child = proc.spawn( 'node', [ appName + '/index.js' ], options );
	// ... and dereference it so it will run detached from this process
	child.unref();
	fs.writeFile( pidfile, child.pid );
	console.log( 'Service started with PID #' + child.pid );
};

try {
	pid = '' + fs.readFileSync( pidfile );
} catch( e ) {}

switch( process.argv[ 3 ] ) {
	case 'start':
		if( pid ) console.log( 'Already running! Use stop or restart!' );
		else startApp();
		return;
	case 'stop':
		if( pid ) killProc( pid );
		else console.log( 'I am not running, nothing to do!');
		return;
	case 'restart':
		if( pid ) killProc( pid );
		startApp();
		return;
	default:
		console.log( 'Please provide one of the following as single argument: start, stop, restart');
		return;
}
