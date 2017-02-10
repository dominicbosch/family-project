const pyFaces = require('../camera/pythonFaces');
const car = require('../i2c/cardo');

var exports = module.exports = {};
let isRunning = false;
let pollInterval;
let facePosition = 0;
let lastFaceDetect = 0;
let lastObstacleDetect = 0;
let config;
let reqConfig = ['slowDownDistance', 'stopDistance'];

exports.init = function(conf) {
	config = conf || {};
	let miss = [];
	for (var i = 0; i < reqConfig.length; i++) {
		if(config[reqConfig[i]]===undefined) miss.push(reqConfig[i]);
	}
	if(miss.length > 0) return new Promise((r, reject) => {
		reject('Some configuration is missing: '+miss.join(', '));
	})
	let ret = car.init(conf);
	pyFaces.init(conf);

	slowDownDistance = conf.slowDownDistance;

	pyFaces.on('warn', function(d) { console.log('pythonFaces Warning: ', d) });
	pyFaces.on('error', function(d) { console.log('pythonFaces Error: ', d) });
	pyFaces.on('fps', function(d) { console.log('Camera FPS: ', d) });
	pyFaces.on('face', function(d) {
		// the retrieved object of one face is: { id, x, y, w, h, relX, relY, relW, relH }
		// we only look for the first (biggest) face on an image: d[0]===0
		// because the first entry in the array is the face ID on an image
		// IDs are sorted from biggest to smallest
		if(d.id===0) {
			if(conf.v) console.log('Face detected at relX: ', d.relX);
			facePosition = d.relX;
			lastFaceDetect = (new Date()).getTime();
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

// we assume three consecutive obstacle measurements at initialization,
// we got a verified obstacle at a distance of zero.
let numMeasurements = 3;
let frontObstacle = 0;
function pollDistance() {
	frontObstacle = car.getFrontObstacle();
	if(frontObstacle < conf.slowDownDistance) numMeasurements++;
	else numMeasurements = 0;
}

// TODO implement
console.warn('TODO: Implement carController.steerCar!');
function steerCar() {
	if(numMeasurements > 2) console.log('Verified obstacle at '+frontObstacle);

}
setInterval(steerCar, 20); // we adjust the steering every 20ms

