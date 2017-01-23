const pyFaces = require('../pythonFaces');


pyFaces.init({
	cbData: function(data) {
		console.log(data);
	},
	cbError: function(err) {
		console.error(err+'');
	},
	v: true,
	vf: true
});

pyFaces.start();
setTimeout(function() {
	pyFaces.stop();
}, 30000)