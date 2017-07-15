const pyFaces = require('../camera/pythonFaces');


pyFaces.init({
	s: true,
	sa: true,
	v: true,
	vf: true,
	iw: 640,
	ih: 480,
	fr: 5
});
pyFaces.on('warn', function(d) { console.log('pythonFaces Warning: ', d) });
pyFaces.on('error', function(d) { console.log('pythonFaces Error: ', d) });
pyFaces.on('fps', function(d) { console.log('Camera FPS: ', d) });
pyFaces.on('face', function(d) { console.log('Face detected: ', d) });
pyFaces.on('detectfps', function(d) { console.log('Face detection FPS: ', d) });
pyFaces.on('storedface', function(d) { console.log('Face stored: ', d) });
pyFaces.on('storedimage', function(d) { console.log('Image stored: ', d) });
pyFaces.start();
setTimeout(function() {
	pyFaces.stop();
}, 30000)