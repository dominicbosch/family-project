'use strict';

// https://github.com/kaosat-dev/adafruit-i2c-pwm-driver

const cp = require('child_process');
const makePwmDriver = require('./pwmDriver');
const pwmDriver = makePwmDriver({address: 0x40, device: '/dev/i2c-1', debug: false});

// Preparing the object orientation (everything attached to exports is visible from outside)
var exports = module.exports = {};

let requiredConfig = [
	'steerDevice',
	'steerLeft',
	'steerCenter',
	'steerRight',
	'motorDevice',
	'motorBack',
	'motorNeutral',
	'motorForward'
];
let config;

exports.init = function(args) {
	// Setting the PWM frequency and returning this "Promise chain"
	return pwmDriver.init()
		.then(() => pwmDriver.setPWMFreq(60))
		// then initializing the config
		.then(function() {
			let miss = [];
			// Test whether some configuration variables are missing
			for(let i = 0; i < requiredConfig.length; i++) {
				let el = requiredConfig[i];
				if(args[el] === undefined || isNaN(parseInt(args[el]))) miss.push(el);
			}
			let msg = 'Cardo is missing or finding invalid integers in conf variable(s): '+miss.join(', ');
			if(miss.length > 0) throw new Error(msg);
			else config = args;
		});
	// Send a value:
	// pwmDriver.setPWM(channel, on, off);
};

function getRampValue(direction, min, base, max) {
	if(direction < 0) { // towards minimum
		// 		from base, subtract direction towards minimum
		return base-direction*(min-base);

	} else { // stay at base or towards maximum
		// 		from base, add direction towards maximum
		return base+direction*(max-base);
	}
}

/*
 * Steer in direction: left [-1 ... 1] right
 */
exports.setSteering = function(direction) {
	if(!config) throw new Error('Not yet initialized! Please invoke init method first!');
	let val = getRampValue(direction, config.steerLeft, config.steerCenter, config.steerRight);
	pwmDriver.setPWM(config.steerDevice, 0, val);
};

/*
 * Full break!
 */
let isBreaking = true; // Initially the car is hopefully braking...
exports.break = function() {
	if(!config) throw new Error('Not yet initialized! Please invoke init method first!');
			
	// We only need to break if it was not the last action, otherwise we risk
	// moving the car back because it is already standing still
	if(!isBreaking) {
		isBreaking = true;
		// Send full back to stop
		pwmDriver.setPWM(config.motorDevice, 0, config.motorBack);

		// After 100ms send neutral position
		setTimeout(function() {
			pwmDriver.setPWM(config.motorDevice, 0, config.motorNeutral);
		}, 100);
	}
}

/*
 * Speed in direction: backward [-1 ... 1] forward
 */
exports.setSpeed = function(direction) {
	isBreaking = false;
	let val = getRampValue(direction, config.motorBack, config.motorNeutral, config.motorForward);
	pwmDriver.setPWM(config.motorDevice, 0, val);
}

/*
 * This is a good example of an event-driven information handling because
 * the child_process ultrasonic.js will send events about a new obstacle whenever
 * they are detected. Through this we do not need to poll and lock the CPU.
 * This is essential in this example because the ultrasonic device requires
 * quite some time to execute one poll (depends on the distance)
 * 
 * TODO how about putting logic about how often an obstacle needs to be
 * detected consecutively in order to be classified as real obstacle instead of
 * noise. also the distance threshold could be added in order to lower
 * communication overhead, i.e. only notify about really relevant obstacles.
 */

let arrObstacleListeners = [];
let distPoller = cp.fork('ultrasonic.js');
distPoller.on('close', (code) => {
	console.warn('Child process exited with code '+code);
});
distPoller.on('message', (msg) => {
	console.log('got message from child process', msg);
	for (var i = 0; i < arrObstacleListeners.length; i++) {
		arrObstacleListeners[i](msg);
	}
});

exports.onFrontObstacle = function(cb) {
	if((typeof cb) === 'function') arrObstacleListeners.push(cb);
}
