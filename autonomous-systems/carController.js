const pyFaces = require('../camera/pythonFaces');
const car = require('../i2c/cardo');

var exports = module.exports = {};
let isRunning = false;
let pollInterval;
let frontObstacle = 0;
let facePosition = 0;
let lastFaceDetect = 0;

exports.init = function(opts) {
	let ret = car.init(opts);
	pyFaces.init(opts);

	pyFaces.on('warn', function(d) { console.log('pythonFaces Warning: ', d) });
	pyFaces.on('error', function(d) { console.log('pythonFaces Error: ', d) });
	pyFaces.on('fps', function(d) { console.log('Camera FPS: ', d) });
	pyFaces.on('face', function(d) {
		// we only look for the first (biggest) face on an image: d[0]===0
		if(d[0]===0) {
			if(opts.v) console.log('Face detected at relX: ', d[5]);
			facePosition = d[5];
			lastFaceDetect = (new Date()).getTime();
			steerCar();
		}
	});
	pyFaces.on('detecttime', function(d) { console.log('Face detection time '+d+'s = '+(1/d)+' FPS') });

	return ret;
};
exports.start = function() {
	console.log('Started');
	pollInterval = setInterval(pollDistance, 50);
	pyFaces.start();
	isRunning = true;
};
exports.stop = function() {
	console.log('Stopped');
	clearInterval(pollInterval);
	pyFaces.stop();
	isRunning = false;
};

exports.isRunning = () => (isRunning === true);

function pollDistance() {
	console.log('Polling');
	frontObstacle = car.getFrontObstacle();
	steerCar();
}

// TODO implement
console.warn('TODO: Implement carController.steerCar!');
function steerCar() {

}


