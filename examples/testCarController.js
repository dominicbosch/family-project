'use strict';

const car = require('../autonomous_systems/carController');

car.init({
	s: true,
	v: true,
	vf: true,
	iw: 1536,
	ih: 1152,
	steerDevice: 0,
	steerLeft: 200,
	steerCenter: 400,
	steerRight: 500,
	motorDevice: 1,
	motorBack: 200,
	motorNeutral: 400,
	motorForward: 500
})