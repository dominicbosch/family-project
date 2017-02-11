'use strict';

const cp = require('child_process');
const car = require('../i2c/cardo');

car.init({
	steerDevice: 0,
	steerLeft: 200,
	steerCenter: 400,
	steerRight: 500,
	motorDevice: 1,
	motorBack: 200,
	motorNeutral: 400,
	motorForward: 500
})
.then(function() {
	let steer = 0;
	let addSteer = 1;
	function setSteer() {
		if(steer < -1 || steer > 1) {
			addSteer *= -1; // change direction
			console.log('Changing steering direction');
		}
		steer += addSteer*0.005;
		car.setSteering(steer);
	}

	let speed = 0;
	let addSpeed = 1;
	let isBreaking = false;
	function setSpeed() {
		if(speed < 1) {
		// Below full speed:
			if(speed < -1) {
				addSpeed = 1; // change direction
				console.log('Going forward...');
			}
			speed += addSpeed*0.004;
			car.setSpeed(speed);

		} else {
		// if we reached fullspeed:
			if(!isBreaking) {
				isBreaking = true;
				console.log('Reached full speed! Breaking...');
				car.break();
				// After 500ms we start moving backwards
				setTimeout(function() {
					speed = 0;
					addSpeed = -1; // change direction
					isBreaking = false;
					console.log('Going reverse...');
				}, 3000);
			}
		}
	}

	// Start steering:
	let intSteer = setInterval(setSteer, 10); // every 10ms


	// Start Speeding up, breaking and so on:
	let intSpeed = setInterval(setSpeed, 15); // every 15ms

	// // Poll distance
	// let intPoll = setInterval(function() {
	// 	console.log('Obstacle at '+car.getFrontObstacle());
	// }, 1000);


	let pollProcess = cp.spawn('node', ['testDist.js']);
	pollProcess.stdout.on('data', (data) => {

	});

	pollProcess.stderr.on('data', reportError);
	pollProcess.on('close', (code) => {
		reportError('Child process exited with code '+code);
	});

	// Stop everything after 30 seconds
	setTimeout(function() {
		clearInterval(intSteer);
		clearInterval(intSpeed);
		clearInterval(intPoll);
		car.break();
		car.setSteering(0);
	}, 30000);

})
.catch(function(err) {
	console.error(err);
});
