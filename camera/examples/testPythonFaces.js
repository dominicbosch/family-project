const pyFaces = require('../pythonFaces');


pyFaces.init({
	s: true,
	v: true,
	vf: true,
	iw: 2048,
	ih: 1536
});
pyFaces.on('warn', function(d) { console.log('testPythonFaces warn', d) });
pyFaces.on('error', function(d) { console.log('testPythonFaces error', d) });
pyFaces.on('fps', function(d) { console.log('testPythonFaces fps', d) });
pyFaces.on('face', function(d) { console.log('testPythonFaces face', d) });
pyFaces.on('detecttime', function(d) { console.log('testPythonFaces detecttime', d) });
pyFaces.start();
setTimeout(function() {
	pyFaces.stop();
}, 30000)