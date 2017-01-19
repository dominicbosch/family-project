const pyFaces = require('./pythonFaces');

let exports = module.exports = {};
let isRunning = false;

exports.init = function(opts) {
	pyFaces.init(opts);
};
exports.start = function() {
	pyFaces.start();
	isRunning = true;
};
exports.stop = function() {
	pyFaces.stop();
	isRunning = false;
};
exports.isRunning = function() {
	return (isRunning === true);
};




// 	if(line.indexOf(strng='obstc | Verified obstacle in ') > -1) {
// 		broadcast('ultrasonic', parseFloat(extractValue(line, strng, 2)));

// 	} else if(line.indexOf(strng='obstc | Cleared obstacle counter') > -1) {
// 		broadcast('ultrasonic', -1);


// 	// temperature
// 	} else if(line.indexOf(strng='sensr | Temperature: ') > -1) {
// 		broadcast('temperature', parseFloat(extractValue(line, strng, 2)));
		

// 	// accelerator X axis
// 	} else if(line.indexOf(strng='sensr | Accelerator: X=') > -1) {
// 		broadcast('accelerator-x', parseFloat(extractValue(line, strng)));
		

// 	// accelerator Y axis
// 	} else if(line.indexOf(strng='sensr | Accelerator: Y=') > -1) {
// 		broadcast('accelerator-y', parseFloat(extractValue(line, strng)));
		

// 	// accelerator Z axis
// 	} else if(line.indexOf(strng='sensr | Accelerator: Z=') > -1) {
// 		broadcast('accelerator-z', parseFloat(extractValue(line, strng)));
		
		
// 	// Speed
// 	} else if(line.indexOf(strng='MOTOR | FINAL DECISION SENT: ') > -1) {
// 		broadcast('motor', parseInt(extractValue(line, strng)));

// 	} else if(line.indexOf(strng='motor | ') > -1) {
// 		broadcast('motor-status', extractValue(line, strng));

		
// 	// face detection} else if(line.indexOf(strng='steer | Heading straight') > -1) {


// 		broadcast('steer', 0);
// 	} else if(line.indexOf('Camera | FPS: ') > -1) {
// 		broadcast('camera-fps', extractValue(line, strng));
// 	} 

// }