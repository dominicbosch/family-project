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
 * the child_process getDist will send distance events whenever a new measurement
 * took place. Through this we do not need to poll and lock the CPU in the meantime.
 * This is essential in this example because the ultrasonic device requires
 * quite some time to execute one poll (depends on the distance)
 * 
 * TODO how about putting logic about how often an obstacle needs to be
 * detected consecutively in order to be classified as real obstacle instead of
 * noise. also the distance threshold could be added in order to lower
 * communication overhead, i.e. only notify about really relevant obstacles.
 */


let arrDistListeners = [];
exports.onFrontDistance = function(cb) {
	if((typeof cb) === 'function') arrDistListeners.push(cb);
}

// we start the child process
let distPoller = cp.spawn(__dirname+'/getDist', ['5']); // 5ms pause between measurements
distPoller.stdout.on('data', (data) => {
	let arr = data.toString().split('\n');

	if(arr.length > 4) {
		// if this value is high, this might indicate that there is too much buffering
		// between the two processes and we need to pull this straight
		console.log('WARNING! Received '+arr.length
			+' lines at once. We need to fix the inter-process buffering!');
	}

	// We only take the latest measurement and put the the distance listener
	// callbacks on top of the event stack with setTimeout(cb, 0) which will
	// execute them as soon as there are available resources (JS best practice).
	// This will not block the current scope even if one of the callbacks causes
	// heavy CPU or I/O load
	let dist = parseInt(arr[arr.length-1]);
	for (var i = 0; i < arrDistListeners.length; i++) {
		let callback = arrDistListeners[i];
		setTimeout(() => {
			callback(dist);
		}, 0);
	}
});

distPoller.stderr.on('data', (data) => console.log(data+''));
distPoller.on('close', (code) => {
	console.log('Distance Poller exited with code '+code);
});

distPoller.on('error', console.error);
