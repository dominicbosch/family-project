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
const car = require('./carController');

let lastImage;
let lastImagePath;
let hasStarted = false;


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
	socket.emit(car.isRunning() ? 'engine-started' : 'engine-stopped');

	socket.on('disconnect', () => {
		console.log(socket.id+' disconnected!');
	});

});
car.init({
	cb
})

function startEngine() {
	console.log('Received start command!');
	if(!car.isRunning()) car.start();
	io.emit('engine-started');
}

function stopEngine() {
	console.log('Received stop command!');
	if(!car.isRunning()) car.stop();
	io.emit('engine-stopped');
}

function broadcast(cmd, val) {
	io.emit(cmd, val);
	console.log('Broadcasting command='+cmd+', value='+val);
}

chokidar.watch('detected-faces/*.jpg').on('add', path => {
	// Give the raspberry 100ms time to store the image properly before reading it
	// Only needed for huge images...
	if(hasStarted) setTimeout(() => broadcastImage(path), 100);
	else lastImagePath = path;
});
setTimeout(() => {
	hasStarted = true;
	console.log('Initialization finished. loading last image');
	if(lastImagePath) broadcastImage(lastImagePath);
}, 5000);

function broadcastImage(path) {
	console.log('loading new image', path);
	fs.readFile(path, (err, buf) => {
		lastImage = buf.toString('base64');
		io.emit('faceCapture', lastImage);
	});
}
