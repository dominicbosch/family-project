'use strict';

// https://github.com/kaosat-dev/adafruit-i2c-pwm-driver

const makePwmDriver = require('adafruit-i2c-pwm-driver');
const pwmDriver = makePwmDriver({address: 0x40, device: '/dev/i2c-1', debug: false});

// Setting the PWM frequency
pwmDriver.setPWMFreq(60);
// Send a value:
// pwmDriver.setPWM(channel, on, off);

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
	let miss = [];
	// Test whether some configuration variables are missing
	for(let i = 0; i < requiredConfig.length; i++) {
		let el = requiredConfig[i];
		if(args[el] === undefined || isNaN(parseInt(args[el]))) miss.push(el);
	}
	let msg = 'Cardo is missing or finding invalid integers in conf variable(s): '+miss.join(', ');
	if(miss.length > 0) throw new Error(msg);
	else config = args;
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
exports.steer = function(direction) {
	if(!config) throw new Error('Not yet initialized! Please invoke init method first!');
	let val = getRampValue(direction, config.steerLeft, config.steerCenter, config.steerRight);
	pwmDriver.setPWM(config.steerDevice, 0, val);
};

/*
 * Full break!
 */
exports.break = function() {
	if(!config) throw new Error('Not yet initialized! Please invoke init method first!');
	// Send full back to stop
	pwmDriver.setPWM(config.motorDevice, 0, config.motorBack);

	// After 100ms send neutral position
	setTimeout(function() {
		pwmDriver.setPWM(config.motorDevice, 0, config.motorNeutral);
	}, 100);
}

/*
 * Speed in direction: backward [-1 ... 1] forward
 */
exports.speed = function(direction) {
	let val = getRampValue(direction, config.motorBack, config.motorNeutral, config.motorForward);
	pwmDriver.setPWM(config.motorDevice, 0, val);
}

