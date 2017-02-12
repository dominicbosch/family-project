const makePwmDriver = require('adafruit-i2c-pwm-driver')
const pwmDriver = makePwmDriver({address: 0x40, device: '/dev/i2c-1'})

pwmDriver.setPWMFreq(60)

let i = 0;
setInterval(function() {
	i = (i>300) ? 0 : i;
	pwmDriver.setPWM(0, 0, 200+(i++)) // channel, on , off
}, 10)

// pwmDriver.setPWM(0, 0, 300) // channel, on , off
