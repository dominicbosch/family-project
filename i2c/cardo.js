// https://github.com/kaosat-dev/adafruit-i2c-pwm-driver

const makePwmDriver = require('adafruit-i2c-pwm-driver')
const pwmDriver = makePwmDriver({address: 0x40, device: '/dev/i2c-1'})

pwmDriver.setPWMFreq(60)


var i = 0;
function steer() {
	if(++i > 300) i = 0;
	pwmDriver.setPWM(0, 0, 200+i) // channel, on , off
}
setInterval(steer, 10); // every 10ms
