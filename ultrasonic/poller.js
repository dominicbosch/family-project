const cp = require('child_process');

var exports = module.exports = {};

let pythonProcess = null;
let arrEventListeners = [];

// Allow registration of event listeners
exports.onObstacle = function(func) {
	if(typeof func === 'function') {
		arrEventListeners.push(func);
	} else console.error('Invalid onObstacle event handler function');
}

exports.start = function() {
	if(!pythonProcess) {
		// -u flag prevents python process from buffering outputs, thus causing late notifications
		let args = ['-u', __dirname+'/poller.py'];
		pythonProcess = cp.spawn('python', args);
		pythonProcess.stdout.on('data', (data) => {
			let arr = data.toString().split('\n');
			for(let i = 0; i < arr.length; i++) {
				emitEvent(parseFloat(arr[i]) || -1);
			}
		});

		pythonProcess.stderr.on('data', reportError);
		pythonProcess.on('close', (code) => {
			reportError('Child process exited with code '+code);
		});
	} else console.warn('Ultrasonic Poller is already running!');
};

function reportError(data) { console.error('error'+data) }

exports.stop = function(opts) {
	if(pythonProcess) {
		pythonProcess.kill();
		pythonProcess = null;
	} else console.warn('Ultrasonic Poller is not running!');
};

function emitEvent(data) {
	for (let i = 0; i < arrEventListeners.length; i++) {
		// we put the callbacks on top of the event stack with setTimeout(cb, 0) which will
		// execute them as soon as there are available resources (JS best practice).
		// This will not block the current scope even if one of the callbacks causes
		// heavy CPU or I/O load
		setTimeout(() => {
			arrEventListeners[i](data);
		}, 0);
	}
}