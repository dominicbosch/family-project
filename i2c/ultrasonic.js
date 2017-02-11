/*
 * This is meant to be loaded through child_process.fork('ultrasonic.js')
 */

const rpio = require('rpio');
const gpioPin = 16;    // header pin 16 = GPIO port 23

function pollDistance() {
	// rpio.sleep(1); // sleep seconds
	rpio.open(gpioPin, rpio.OUTPUT, rpio.LOW);
	let start = process.hrtime(); // nanoseconds
// console.log(hrTime[0] * 1000000 + hrTime[1] / 1000)

	rpio.write(gpioPin, rpio.HIGH);
	rpio.msleep(1); // sleep milliseconds
	rpio.write(gpioPin, rpio.LOW);
	while(true) {
		
	}
	let end = process.hrtime(); // nanoseconds
	console.log(end-start); // passed nanoseconds
	setTimeout(pollDistance, 5); // release the CPU for 5ms after polling
}


pollDistance(); // Start polling