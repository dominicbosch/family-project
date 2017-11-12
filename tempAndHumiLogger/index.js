const fs = require('fs');
const sensor = require('node-dht-sensor');
const http = require('http');
const WebSocket = require('ws');
const express = require('express');

const conf = [
	{ pin: 5, type: 11, id: 'DHT11 #1' },
	{ pin: 6, type: 11, id: 'DHT11 #2' },
	{ pin: 12, type: 22, id: 'AM2302' }
];
const currVals = {};

const app = express();
const server = http.createServer(app);
const wss = new WebSocket.Server({ server });

app.use('/', express.static(__dirname+'/www'));

// this will be quite an intensive task once the logs get bigger:
app.get('/getlogs', function(req, res){
	let start = process.hrtime();
	Promise.all(conf.map(d => fetchLog(d)))
		.then((arr) => {
			console.log('Log fetching took %d', start-process.hrtime())
			res.send(arr);
		});
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
	return newPromise(function(resolve, reject) {
		fs.readFile(dataLogPath(sens), (err, data) => {
			if(err) reject(err);
			else resolve({
				sensor: sens,
				data: JSON.parse(data)
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
				client.send(currVals);
			});
			fs.appendFileSync(dataLogPath(sens), ts+','+temp+','+humi);
		}
	});
}



server.listen(8080, function listening() {
	console.log('Listening on %d', server.address().port);
});

// Do it initially and then every ten seconds
runAllSensors();
setInterval(runAllSensors, 10000);