const pyFaces = require('../camera/pythonFaces');
const car = require('../i2c/cardo');

var exports = module.exports = {};
let config;
let isRunning = false;
let steerInterval;
let facePosition = 0;
let lastFaceDetect = 0;
let rampUpFace = 0;
let lastObstacleDetect = 0;
let reqConfig = ['slowDownDistance', 'stopDistance'];

exports.init = function(conf) {
	config = conf || {};
	let miss = [];
	for (var i = 0; i < reqConfig.length; i++) {
		if(config[reqConfig[i]]===undefined) miss.push(reqConfig[i]);
	}
	// This is an interesting way to return a rejected promise :-P
	if(miss.length > 0) return new Promise((r, reject) => {
		reject('Some configuration is missing: '+miss.join(', '));
	});

	if(config.v) console.log('Initializing with comfig:\n'+JSON.strinigfy(config, null, 2));
	let ret = car.init(config);
	pyFaces.init(config);

	pyFaces.on('warn', function(d) { console.log('pythonFaces Warning: ', d) });
	pyFaces.on('error', function(d) { console.log('pythonFaces Error: ', d) });
	pyFaces.on('fps', function(d) { console.log('Camera FPS: ', d) });
	pyFaces.on('face', function(d) {
		// the retrieved object of one face is: { id, x, y, w, h, relX, relY, relW, relH }
		// we only look for the first (biggest) face on an image: d.id === 0
		// IDs are sorted from biggest to smallest
		if(d.id === 0) {
			if(config.v) console.log('Face detected at relX: ', d.relX);
			facePosition = d.relX;
			lastFaceDetect = (new Date()).getTime();
			if(rampUpFace === 0) rampUpFace = lastFaceDetect;
		}
	});
	pyFaces.on('detecttime', function(d) { console.log('Face detection time '+d+'s = '+(1/d)+' FPS') });

	return ret;
};
exports.start = function() {
	if(config.v) console.log('CarController started!');
	steerInterval = setInterval(adjustCarControls, 50);
	pyFaces.start();
	isRunning = true;
};
exports.stop = function() {
	if(config.v) console.log('CarController stopped!');
	clearInterval(steerInterval);
	pyFaces.stop();
	isRunning = false;
};

exports.isRunning = () => (isRunning === true);

// we assume three consecutive obstacle measurements at initialization,
// which means we got a verified obstacle at a distance of zero.
let numMeasurements = 3;
let frontObstacle = 0;
let speedUpTime = 1000; // we speed up over 1000ms
let speedStayTime = 3000; // we stay at full speed for 3000ms
let speedStopTime = 10000; // we slow down and stop until 10000ms passed
function adjustCarControls() {
	
	// Test for obstacles
	frontObstacle = car.getFrontObstacle();
	if(frontObstacle < config.slowDownDistance) numMeasurements++;
	else numMeasurements = 0;

	let now = (new Date()).getTime();
	let timePassed = now - lastFaceDetected;

	// we are ramping up towards full speed 
	if(now-rampUpFace < speedUpTime) {


	// we stay at full speed while no faces are detected 
	} else if(now-lastFaceDetected < speedStayTime) {


	// we slow down since no ore faces were detected 
	} else if(now-lastFaceDetected < speedStopTime) {
		rampUpFace = 0;
	} else {
		if(config.v) console.log('Breaking because no more faces!');
		car.break();
	}

	if(numMeasurements > 2) {
		if(config.v) console.log('Verified obstacle at '+frontObstacle);
	}
}

/*
# We need to know whether we are already ramping up, so that new pictures 
# are not causing an immediate slow down
def adjustSpeed():
	global rampUpFace
	now = time.time()

	# how much time since the last face detection passed 
	timePassed = now - lastFaceDetected
	writeLog('faces | Last face detected {:.2f}s ago'.format(timePassed))
	# the last face was only 1 second ago detected, we speed up
	# if we are already in a speedup ramp we do not adjust to latest picture!
	if timePassed < 1*timeFactor and now-rampUpFace < rampUpTime:
		# speedup with linear ramp over one second!
		arduinoValue = motorNeutral-(motorNeutral-motorFull)*timePassed/3
		writeLog('motor | Speeding up!')

	# between 1 to 3 seconds since lasg face detected we stay at full speed
	elif timePassed < 3*timeFactor:
		arduinoValue = motorFull
		writeLog('motor | Staying at full speed!')

	# if more than 3 seconds passed since last face detected, 
	# we gradually slow down over the next seven seconds until we stop
	elif timePassed < 10*timeFactor:
		# we reset the ramp up face
		rampUpFace = 1
		
		# 10 is full speed, the other 90 (to reach 100, which is stop)
		# are spread over ten seconds
		arduinoValue = motorFull+(motorNeutral-motorFull)*timePassed/10
						# 70				100			70			
		writeLog('motor | Slowing down because no more face detected')

	# if the last face has been detected more than 10 seconds ago, we stay still
	else:
		arduinoValue = motorBreak
		writeLog('motor | !BREAKING! because no faces')

	# if more than twice an obstacle has been detected we slow down if we are not already breaking
	if arduinoValue != motorBreak and numMeasurements > 2:
		if ultrasonic < slowDownDistance:
			writeLog('motor | obstacle in: {}cm'.format(ultrasonic))
			# slow down with a linear ramp y = m*x + b defined above.
			# if it is far away, the value would be under motorFull, thus we take
			# the maximum value in order to not send negative numbers to the arduino command
			arduinoValue = max(m*ultrasonic+b, motorFull)
			# writeLog('us={}, m={}, b={}, mF={}, aV={}, '.format(ultrasonic, m, b, motorFull, arduinoValue))
			if arduinoValue > motorNeutral:
				# if we are closer than neutral position, we break
				arduinoValue = motorBreak
				writeLog('motor | !BREAKING! because of obstacle')
			else:
				writeLog('motor | Slowing down because of obstacle')

	writeLog('MOTOR | FINAL DECISION SENT: {}'.format(int(arduinoValue)))
	commandArduino(motorDevice, arduinoValue)


def adjustSteering():
	now = time.time()
	
	# how much time since the last face detection passed 
	timePassed = now - lastFaceDetected
	relX = lastRelativeFacePosition
	writeLog('steer | time since last face {:.2f}s'.format(timePassed))

	# if we are still in valid turn time, we turn
	if timePassed < turnTime*timeFactor:
		if relX < 0:
			cmd = servoCenter+(servoCenter-servoLeft)*relX #relX will be negative
			# writeLog("steering left {}% = command to arduino: {}".format(relX*100, cmd))
			commandArduino(servoDevice, cmd)

		else:
			cmd = servoCenter+(servoRight-servoCenter)*relX
			# writeLog("steering right {}% = command to arduino: {}".format(relX*100, cmd))
			commandArduino(servoDevice, cmd)
		writeLog('STEER | TURNING: {}'.format(int(cmd)))

	# if we are under the detect time we assume we are heading the right direction, thus we stop turning
	elif timePassed < avgDetectTime*timeFactor:
		writeLog('steer | Heading straight')
		commandArduino(servoDevice, servoCenter)

	# if turn time passed, we don't know what to do anymore. So we start going left right
	else:
		writeLog('steer | TODO should go left, right, left,... until new face detected or stop')
		pass
		# print "else"
	# use sinus if face hasnt been detected for 3 seconds
	# steering will do a bit of left right left in order to acquire a new target
	
	# math.sin([0 .. 2*math.pi]) => left -> right -> center
	
	# we need to steer double the time to the right than to the left because we want to be
	# turning over the center

	# when all the way to the left again (5/2*math.pi) we stay for a full turn at the end
	
	# else head towards the face
*/