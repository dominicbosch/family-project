const cp = require('child_process');

var exports = module.exports = {};

let pythonProcess = null;
let cbData;
let cbError;
let options;

function reportError(data) {
	if(typeof cbError === 'function') {
		cbError(data);
	} else console.warn('No Error handler attached to pythonFaces!')
}

exports.init = function(opts) {
	options = opts || {};
	cbData = opts.cbData;
	cbError = opts.cbError;
};
exports.start = function() {
	if(!pythonProcess) {
		// -u flag prevents python process from buffering outputs, thus causing late notifications
		let args = ['-u', _dirname+'/lookForFaces.py'];
		if(options.hf) args.push('-hf');
		if(options.vf) args.push('-vf');
		if(options.v) args.push('-v');
		if(options.cf) args.push('--cf', options.cf);
		if(options.iw) args.push('--iw', options.iw);
		if(options.ih) args.push('--ih', options.ih);
		if(options.path) args.push('-savepath', options.path);
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
	} else console.log('Face detection is already running!')
};
exports.stop = function(opts) {
	if(pythonProcess) {
		pythonProcess.kill();
		pythonProcess = null;
	} else console.log('Face detection is not running!')
};
exports.isRunning = function(opts) {
	return (pythonProcess !== null);
};

function processLine(line) {
	if(typeof cbData === 'function') {
		if(line.indexOf('New face(s) detected ') > -1) {
			// let strng = ', nearest at ';
			// broadcast('steer', parseFloat(extractValue(line, strng, 1)));
		} else if(line.indexOf('#') > -1) {
			cbData(extractValue(line, '#', 1).split('|'));
		}	
	}
}

function extractValue(line, str, cutoff) {
	let ret = line  // From the whole line
		.substr(line.indexOf(str)+str.length); // start at the end of the searched string
	if(cutoff) ret = ret.slice(0, -cutoff); // cut away this many characters at the end
	return ret;
}
