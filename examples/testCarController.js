'use strict';

const car = require('../autonomous-systems/carController');

car.init({
	s: true,
	v: true,
	vf: true,
	iw: 1024,
	ih: 768,
	steerDevice: 0,
	steerLeft: 200,
	steerCenter: 400,
	steerRight: 500,
	motorDevice: 1,
	motorBack: 200,
	motorNeutral: 400,
	motorForward: 500,
	slowDownDistance: 80,
	stopDistance: 20,
	obstacleCount: 2,
	turnTime: 500,
	speedUpTime: 3000,
	stayTime: 5000,
	stopTime: 10000
})
.then(car.start)
.catch((err) => {
	console.error('Couldn\'t start car!', err)
});
