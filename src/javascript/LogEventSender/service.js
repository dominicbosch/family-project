var getPID, pid, killProc, child, out, err, startApp,
	fs = require( 'fs' ),
	proc = require( 'child_process' ),
	pidfile = 'LogEventSender.pid';

killProc = function( pid ) {
	try {
		process.kill( pid );
		console.log( 'Process #' + pid + ' killed' );
	} catch( e ) {
		console.log( 'Process not killed?' );
	}
	fs.unlink( pidfile, function( err ) {
		if( err ) console.log( err );
	});
};

startApp = function() {
	fs.unlink( './log.txt', function( err ) {
		if( err ) console.log( err );
	});
	out = fs.openSync( './log.txt', 'a' );
	err = fs.openSync( './log.txt', 'a' );
	child = proc.spawn( 'node', ['index.js'], { detached: true, stdio: [ 'ignore', out, err ] } );
	child.unref();
	fs.writeFile( pidfile, child.pid );
	console.log( 'Service started with PID #' + child.pid );
};

try {
	pid = '' + fs.readFileSync( pidfile );
} catch( e ) {}

switch( process.argv[ 2 ] ) {
	case 'start':
		startApp();
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
