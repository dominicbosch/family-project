/*
 * This is meant to be loaded through child_process.fork('ultrasonic.js')
 */

const rpio = require('rpio');
const trigPin = 16;    // Trigger pin 16 = GPIO port 23
const echoPin = 18; 	// Echo Pin 18 = GPIO port 24

rpio.open(trigPin, rpio.OUTPUT, rpio.LOW);
rpio.open(trigPin, rpio.INPUT);

function pollDistance() {
	

	console.log('Initiating GPIO')
	rpio.write(trigPin, rpio.HIGH);
	rpio.usleep(10); // sleep milliseconds
	rpio.write(trigPin, rpio.LOW);

	console.log('Waiting for echoPin')

	// rpio.sleep(1); // sleep seconds
	let start = process.hrtime()[1]; // nanoseconds
    // console.log(hrTime[0] * 1000000 + hrTime[1] / 1000)

	let val = rpio.read(echoPin);
	console.log(val);
	let txt = '';
	let i = 0;
	while(!(val = rpio.read(echoPin))) {
		txt += val;
		if(i++ === 500) {
			console.log(txt);
			txt = '';
			i = 0;
		}
	}

	let end = process.hrtime()[1]; // nanoseconds
	console.log((end-start)/58000); // passed nanoseconds
	setTimeout(pollDistance, 5); // release the CPU for 5ms after polling
}


pollDistance(); // Start polling