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

lineReader.on('line', function (line) {
	if(line[0] === '[') {
		let ts = line.substr(1, 13);
		let txt = line.substr(16);
		if(txt.indexOf('storedimage') > -1) {
			console.log('image: '+txt.substr(13))
			sharp('../camera/snapshots/snap_2017.07.13_06:54:16.jpg')
				.resize(320, 240)
				.toFile('www/thumbs/'+'snap_2017.07.13_06:54:16.jpg', (err, info) => {
					console.log(err, info)
				})
		}
		if(txt.indexOf('storedface') > -1) {
			console.log('face: '+txt.substr(12))
		}
	} else {
		console.log('No timestamp in log:', line);
	}
});

app.use(express.static(__dirname+'/www'));

app.listen(8080, () => {
	console.log('Serving on port 8080!');
});
