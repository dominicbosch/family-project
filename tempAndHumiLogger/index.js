const fs = require('fs');
const sensor = require('node-dht-sensor');
const http = require('http');
const WebSocket = require('ws');
const express = require('express');

const conf = [
	{ pin: 5, type: 11, id: 'DHT11 #1', w: 0.1 },
	{ pin: 6, type: 11, id: 'DHT11 #2', w: 0.1 },
	{ pin: 12, type: 22, id: 'AM2302', w: 0.4 }
];
const currVals = {};

const app = express();
const server = http.createServer(app);
const wss = new WebSocket.Server({ server });

// TODO add sophisticated preprocessor that aggregates data over longer time periods
// TODO it will not make sense to average more than an hour
// TODO maybe show standard deviations per hour?
// TODO maybe overlay day cycles with greying out?

app.use('/', express.static(__dirname+'/www'));

// this will be quite an intensive task once the logs get bigger:
app.get('/getlogs', function(req, res){
	var start = process.hrtime();
	Promise.all(conf.map(fetchLog))
		.then((arr) => {
			let at = process.hrtime(start);
			console.log('Log fetching took %ds %dms', at[0], at[1]/1e6)
			res.send(arr);
		})
		.catch(console.error);
});

// Standard reply to all nonsense:
// app.use(function (req, res) {
// 	res.send(currVals);
// });

// if new client connects to socket he immediately receives the latest data
wss.on('connection', function(ws, req) {
	ws.send(JSON.stringify(currVals));
});

function dataLogPath(sens) {
	return __dirname+'/datalogs/data_pin'+sens.pin+'_type'+sens.type+'.csv';
}

function fetchLog(sens) {
	return new Promise(function(resolve, reject) {
		fs.readFile(dataLogPath(sens), (err, data) => {
			if(err) reject(err);
			else resolve({
				sensor: sens,
				data: data.toString().split('\n').map((d) => d.split(','))
			});
		})
	});
}

function runAllSensors() {
	for (let i = 0; i < conf.length; i++) {
		readSensorAndStore(conf[i]);
	}
}

function readSensorAndStore(sens) {
	sensor.read(sens.type, sens.pin, function(err, temp, humi) {
		if (!err) {
			temp = temp.toFixed(2);
			humi = humi.toFixed(2);
			let ts = (new Date()).getTime();
			currVals[sens.id] = {
				temp: temp,
				humi: humi,
				ts: ts
			};
			wss.clients.forEach(function(client) {
				client.send(JSON.stringify(currVals));
			});
			fs.appendFileSync(dataLogPath(sens), ts+','+temp+','+humi);
		}
	});
}



server.listen(8080, function listening() {
	console.log('Listening on %d', server.address().port);
});

// Do it initially and then every minute
runAllSensors();
setInterval(runAllSensors, 60 * 1000);