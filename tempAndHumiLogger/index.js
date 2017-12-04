const noSensor = process.argv.indexOf('-n') > -1;

const fs = require('fs');
if (!noSensor) {
	const sensor = require('node-dht-sensor');
}
const http = require('http');
const WebSocket = require('ws');
const express = require('express');

const conf = [
	{ pin: 5, type: 11, id: 'DHT11-1', w: 0.1 },
	{ pin: 6, type: 11, id: 'DHT11-2', w: 0.1 },
	{ pin: 12, type: 22, id: 'AM2302', w: 0.4 }
];


const app = express();
const server = http.createServer(app);
const wss = new WebSocket.Server({ server });

// if new client connects to socket he immediately receives the conf and latest data
const currVals = {};
wss.on('connection', function(ws, req) {
	ws.send(JSON.stringify({ conf: conf }));
	ws.send(JSON.stringify({ data: currVals }));
});

// TODO add sophisticated preprocessor that aggregates data over longer time periods
// TODO it will not make sense to average more than an hour
// TODO maybe show standard deviations per hour?
// TODO maybe overlay day cycles with greying out?

app.use('/', express.static(__dirname+'/www'));

app.get('/logs', (req, res) => {
	fs.readdir(__dirname+'/datalogs', (err, files) => {
		if(err) res.status(404).send(err.message);
		else {
			let arr = files.filter(d => d.substr(0, 7) === 'sensor_');
			let obj = {};
			for (let i = 0; i < arr.length; i++) {
				let dt = arr[i].split('_')[2].substr(0, 10);
				obj[dt] = 1;
			}
			res.send(Object.keys(obj));
		}
	});
});

// this will be quite an intensive task once the logs get bigger:
app.get('/log/:day', function(req, res) {
	fs.readdir(__dirname+'/datalogs', (err, files) => {
		let arr = files.filter(d => {
			let a = d.split('_');
			if (a.length < 3) return false;
			return a[2].substr(0, 10) === req.params.day;
		});
		Promise.all(arr.map(fetchLog))
			.then((arr) => res.send(arr) )
			.catch(console.error);
	});
});

function fetchLog(fileName) {
	return new Promise((resolve, reject) => {
		let id = fileName.split('_')[1];
		let cid = conf.map(s => s.id).indexOf(id);
		fs.readFile(__dirname+'/datalogs/'+fileName, (err, data) => {
			if(err) reject(err);
			else resolve({
				sensor: conf[cid],
				data: data.toString().split('\n').map(d => d.split(','))
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
	let ts = (new Date()).getTime(); // to ensure same timestamp for all
	let dt = new Date().toISOString().substr(0, 10);
	sensor.read(sens.type, sens.pin, (err, temp, humi) => {
		if (!err) {
			temp = temp.toFixed(2);
			humi = humi.toFixed(2);
			currVals[sens.id] = {
				temp: temp,
				humi: humi,
				ts: ts
			};
			let txt = JSON.stringify({ data: currVals });
			wss.clients.forEach((client) => client.send(txt));
			let path = __dirname+'/datalogs/sensor_'+sens.id+'_'+dt+'.csv';
			fs.appendFileSync(path, ts+','+temp+','+humi+'\n');
		}
	});
}

server.listen(8080, () => console.log('Listening on '+server.address().port));

if (!noSensor) {
	// Do it initially and then every minute
	runAllSensors();
	setInterval(runAllSensors, 60 * 1000);
}