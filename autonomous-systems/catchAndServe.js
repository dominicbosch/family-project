/*
 * Load required libraries and wire them.
 * These libraries are constantly linked to the variables.
 */
const fs = require('fs');
const path = require('path');
const express = require('express');
const app = express();
const server = require('http').Server(app);
const io = require('socket.io')(server);
const cp = require('child_process');
const chokidar = require('chokidar');

let lastImage, pythonProcess;


// Mir serviere alli website us family-project/visualizations/www
app.use('/', express.static(path.resolve('..', 'visualizations', 'www')));

// D Website findet me uf http://[raspberry-IP]:8080
server.listen(8080, () => {
	console.log('Serving on port 8080!');
});

io.on('connection', (socket) => {
	console.log('Client connected on socket from IP "'+socket.conn.remoteAddress
		+'" and has been assigned the SocketID "'+socket.id+'"');

	// When a client connects we send the last picture
	if(lastImage) io.emit('faceCapture', lastImage);

	socket.on('engine-start', startEngine);
	socket.on('engine-stop', stopEngine);
	socket.emit(pythonProcess ? 'engine-started' : 'engine-stopped');

	socket.on('disconnect', () => {
		console.log(socket.id+' disconnected!');
	});

});

function startEngine() {
	console.log('Received start command!');
	if(!pythonProcess) {
		pythonProcess = cp.spawn('python', ['-u', 'steer-car.py', '-s']);
		pythonProcess.stdout.on('data', (data) => {
			let arr = data.toString().split('\n');
			for(let i = 0; i < arr.length; i++) processLine(arr[i]);
		});

		pythonProcess.stderr.on('data', (data) => {
			console.log(`stderr: ${data}`);
		});

		pythonProcess.on('close', (code) => {
			console.log(`child process exited with code ${code}`);
		});
	}
	io.emit('engine-started');
}

function stopEngine() {
	console.log('Received stop command!');
	if(pythonProcess) {
		pythonProcess.kill();
		pythonProcess = null;
	}	
	io.emit('engine-stopped');
}

function processLine(line) {
	let strng;
	// console.log(line);

	// ultrasonic
	if(line.indexOf(strng='obstc | Verified obstacle in ') > -1) {
		broadcast('ultrasonic', parseFloat(extractValue(line, strng, 2)));

	} else if(line.indexOf(strng='obstc | Cleared obstacle counter') > -1) {
		broadcast('ultrasonic', -1);


	// temperature
	} else if(line.indexOf(strng='sensr | Temperature: ') > -1) {
		broadcast('temperature', parseFloat(extractValue(line, strng, 2)));
		

	// accelerator X axis
	} else if(line.indexOf(strng='sensr | Accelerator: X=') > -1) {
		broadcast('accelerator-x', parseFloat(extractValue(line, strng)));
		

	// accelerator Y axis
	} else if(line.indexOf(strng='sensr | Accelerator: Y=') > -1) {
		broadcast('accelerator-y', parseFloat(extractValue(line, strng)));
		

	// accelerator Z axis
	} else if(line.indexOf(strng='sensr | Accelerator: Z=') > -1) {
		broadcast('accelerator-z', parseFloat(extractValue(line, strng)));
		
		
	// Speed
	} else if(line.indexOf(strng='MOTOR | FINAL DECISION SENT: ') > -1) {
		broadcast('motor', parseInt(extractValue(line, strng)));

	} else if(line.indexOf(strng='motor | ') > -1) {
		broadcast('motor-status', extractValue(line, strng));

		
	// face detection
	} else if(line.indexOf('faces | new face(s) detected ') > -1) {
		strng = ', nearest at ';
		broadcast('steer', parseFloat(extractValue(line, strng, 1)));
		
	} else if(line.indexOf(strng='steer | Heading straight') > -1) {
		broadcast('steer', 0);
	} 

}

function broadcast(cmd, val) {
	io.emit(cmd, val);
	console.log('Broadcasting command='+cmd+', value='+val);
}

function extractValue(line, str, cutoff) {
	let ret = line  // From the whole line
		.substr(line.indexOf(str)+str.length); // start at the end of the searched string
	if(cutoff) ret = ret.slice(0, -cutoff); // cut away this many characters at the end
	return ret;
}

// One-liner for current directory, ignores .dotfiles
chokidar.watch('detected-faces/*').on('add', path => {
	console.log('new file', path);
	// Give the raspberry 100ms time to store the image properly before reading it
	// Only needed for huge images...
	setTimeout(() => {
		fs.readFile(path, (err, buf) => {
			lastImage = buf.toString('base64');
			io.emit('faceCapture', lastImage);
		});
	}, 100);
});
