const pyFaces = require('../pythonFaces');


pyFaces.init({
	s: true,
	v: true,
	vf: true,
	iw: 1536,
	ih: 1152
});
pyFaces.on('warn', function(d) { console.log('pythonFaces Warning: ', d) });
pyFaces.on('error', function(d) { console.log('pythonFaces Error: ', d) });
pyFaces.on('fps', function(d) { console.log('Camera FPS: ', d) });
pyFaces.on('face', function(d) { console.log('Face detected: ', d) });
pyFaces.on('detecttime', function(d) { console.log('Face detection time '+d+'s = '+1/d+' FPS') });
pyFaces.start();
setTimeout(function() {
	pyFaces.stop();
}, 30000)