const fs = require('fs');
const sensor = require('node-dht-sensor');

const conf = [
	{ pin: 5, type: 11 },
	{ pin: 6, type: 11 },
	{ pin: 12, type: 22 }
];


function runAllSensors() {
	for (let i = 0; i < conf.length; i++) {
		readSensorAndStore(conf[i].pin, conf[i].type);
	}
}

function readSensorAndStore(pin, type) {
	sensor.read(type, pin, function(err, temp, humi) {
		if (!err) {
			temp = temp.toFixed(2);
			humi = humi.toFixed(2);
			let ts = (new Date()).getTime();
			let name = 'data_pin'+pin+'_type'+type+'.csv';
			fs.appendFileSync(name, ts+','+temp+','+humi);
		}
	});
}
// Do it initially and then every ten seconds
runAllSensors();
setInterval(runAllSensors, 10000);
