const fs = require('fs');
const path = require('path');
const readline = require('readline');
const express = require('express');
const app = express();
const sharp = require('sharp');

if(process.argv.length <= 2) {
	return console.error('Provide a log file as an argument');
}

let filepath, lineReader;
try {
	filepath = path.resolve(process.argv[2])
	console.log('Trying to open "'+filepath+'"');
	lineReader = readline.createInterface({
		input: fs.createReadStream(filepath)
	});

} catch(err) {
	return console.error(err);
}
let obj = {
	faces: [],
	snapshots: [],
	facedetect: [],
	motorstate: [],
	steering: [],
	speed: [],
	ultrasonic: [],
	camerafps: [],
	detectfps: []
};
let motorStates = {
	accelerating: 'Accelerating because face detected!',
	fullspeed: 'Staying at full speed!',
	slowdown: 'Slowing down because no more faces!',
	nofacebreak: 'Breaking because no faces!',
	obstacle: 'Slowing down because of obstacle!',
	obstaclebreak: 'Breaking because of obstacle!'
}

// Parse the log file and put the data in the correct objectS
lineReader.on('line', function (line) {
	if(line[0] === '[') {
		let ts = parseInt(line.substr(1, 13));
		if(obj.tsmin === undefined) obj.tsmin = obj.tsmax = ts;
		if(obj.tsmin > ts) obj.tsmin = ts;
		if(obj.tsmax < ts) obj.tsmax = ts;
		let txt = line.substr(16);
		if(txt.indexOf('storedimage') > -1) {
			let img = txt.substr(13);
			sharp('../camera/snapshots/'+img)
				.resize(480, 360)
				.toFile('www/thumbs/'+img, (err, info) => {
					if(err) console.warn(err);
					else obj.snapshots.push({
						ts: ts,
						img: img
					})
				})
		} else if(txt.indexOf('storedface') > -1) {
			let img = txt.substr(12);
			sharp('../camera/detected-faces/'+img)
				.resize(480, 360)
				.toFile('www/thumbs/'+img, (err, info) => {
					if(err) console.warn(err);
					else obj.faces.push({
						ts: ts,
						img: img
					})
				})
		} else if(txt.indexOf('facedetected') > -1) {
			obj.facedetect.push({ ts: ts, val: parseFloat(txt.substr(14)) });

		} else if(txt.indexOf('motorstate') > -1) {
			obj.motorstate.push({ ts: ts, val: motorStates[txt.substr(12)] });

		} else if(txt.indexOf('steering') > -1) {
			obj.steering.push({ ts: ts, val: parseFloat(txt.substr(10)) });

		} else if(txt.indexOf('speed') > -1) {
			obj.speed.push({ ts: ts, val: parseFloat(txt.substr(7)) });

		} else if(txt.indexOf('ultrasonic') > -1) {
			obj.ultrasonic.push({ ts: ts, val: parseFloat(txt.substr(12)) });

		} else if(txt.indexOf('camerafps') > -1) {
			obj.camerafps.push({ ts: ts, val: parseFloat(txt.substr(11)) });

		} else if(txt.indexOf('detectfps') > -1) {
			obj.detectfps.push({ ts: ts, val: parseFloat(txt.substr(11)) });

		} else {
			console.warn('NOT HANDLED: '+line);
		}
	} else {
		console.log('NOT HANDLED: '+line);
	}
});

app.use(express.static(__dirname+'/www'));
app.get('/log.json', (req, res) => res.send(obj));

app.listen(8080, () => {
	console.log('Serving on port 8080!');
});
