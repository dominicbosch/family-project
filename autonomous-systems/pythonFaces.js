
let exports = module.exports = {};

let pythonProcess = null;
let cbData;
let cbError;

function reportError(data) {
	if(typeof cbError === 'function') {
		cbError(data);
	} else console.warn('No Error handler attached to pythonFaces!')
}

exports.init = function(opts) {
	opts = opts || {};
	cbData = opts.cbData;
	cbError = opts.cbError;
};
exports.start = function() {
	if(!pythonProcess) {
		// -u flag prevents python process from buffering outputs, thus causing late notifications
		pythonProcess = cp.spawn('python', [
			'-u',
			'../camera/lookForFaces.py',
			
		]);
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
			let strng = ', nearest at ';
			broadcast('steer', parseFloat(extractValue(line, strng, 1)));
		}	
	}
}

function extractValue(line, str, cutoff) {
	let ret = line  // From the whole line
		.substr(line.indexOf(str)+str.length); // start at the end of the searched string
	if(cutoff) ret = ret.slice(0, -cutoff); // cut away this many characters at the end
	return ret;
}
