const sensor = require('node-dht-sensor');

const conf = [
	{ pin: 5, type: 11 },
	{ pin: 6, type: 11 },
	{ pin: 12, type: 22 }
];

setInterval(function() {
	for (let i = 0; i < conf.length; i++) {
		readSensorAndStore(conf[i].pin, conf[i].type);
	}
}, 10000);

function readSensorAndStore(pin, type) {
	sensor.read(pin, type, function(err, temp, humi) {
		if (!err) {
			temp = temp.toFixed(2);
			humi = humi.toFixed(2);
			fs.appendFileSync('data_pin'+pin+'_type'+type+'csv', temp+','+humi);
		}
	});
}
