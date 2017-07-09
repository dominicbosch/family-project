const cp = require('child_process');

var exports = module.exports = {};

let pythonProcess = null;
let eventListeners = {};
let options;


exports.init = function(opts) {
	options = opts || {};
};

// Allow registration of event listeners
exports.on = function(evt, func) {
	if(['warn', 'error', 'face', 'fps', 'detecttime', 'storedimage', 'storedface'].indexOf(evt) === -1) {
		console.error('Unknown event: '+evt);
	} else if(typeof func === 'function') {
		if(!eventListeners[evt]) eventListeners[evt] = [];
		eventListeners[evt].push(func);
	} else console.error('Invalid event handler function for event '+evt);
}
exports.start = function() {
	if(!pythonProcess) {
		// -u flag prevents python process from buffering outputs, thus causing late notifications
		// we need the -v flag in order to fet the detect time and FPS info
		let args = ['-u', __dirname+'/lookForFaces.py', '-v'];
		if(options.s) args.push('-s');
		if(options.hf) args.push('-hf');
		if(options.vf) args.push('-vf');
		if(options.cf) args.push('--cf', options.cf);
		if(options.iw) args.push('--iw', options.iw);
		if(options.ih) args.push('--ih', options.ih);
		pythonProcess = cp.spawn('python', args);
		pythonProcess.stdout.on('data', (data) => {
			let arr = data.toString().split('\n');
			for(let i = 0; i < arr.length; i++) {
				processLine(arr[i]);
			}
		});

		pythonProcess.stderr.on('data', reportError);
		pythonProcess.on('close', (code) => {
			reportError('Child process exited with code '+code);
		});
	} else emitEvent('warn', 'Face detection is already running!');
};

function reportError(data) { emitEvent('error', data+'') }

exports.stop = function(opts) {
	if(pythonProcess) {
		pythonProcess.kill();
		pythonProcess = null;
	} else emitEvent('warn', 'Face detection is not running!');
};
exports.isRunning = function(opts) {
	return (pythonProcess !== null);
};

let arrFaceKeys = ['id', 'x', 'y', 'w', 'h', 'relX', 'relY', 'relW', 'relH'];
function processLine(line) {
	if(line.indexOf(strng='Camera | FPS: ') > -1) {
		emitEvent('fps', parseFloat(extractValue(line, strng)));
	} else if(line.indexOf(strng='FaceDetect | Detect Time: ') > -1) {
		emitEvent('detecttime', parseFloat(extractValue(line, strng)));
	} else if(line.indexOf('#') > -1) {
		let oFace = {};
		let arrVals = extractValue(line, '#').split('|').map(parseFloat);
		// Map the values array into a face object with keys as defined in arrFaceKeys
		for(let i = 0; i < arrFaceKeys.length; i++) {
			oFace[arrFaceKeys[i]] = arrVals[i];
		}
		emitEvent('face', oFace);
	} else if(line.indexOf(strng='Stored Image to: ') > -1) {
		emitEvent('storedimage', line.substr(str.length));

	} else if(line.indexOf(strng='Stored Face to: ') > -1) {
		emitEvent('storedface', line.substr(str.length));

	}
}

function extractValue(line, str, cutoff) {
	let ret = line  // From the whole line
		.substr(line.indexOf(str)+str.length); // start at the end of the searched string
	if(cutoff) ret = ret.slice(0, -cutoff); // cut away this many characters at the end
	return ret;
}

function emitEvent(evt, data) {
	for (let i = 0; i < eventListeners[evt].length; i++) {
		eventListeners[evt][i](data);
	}
}