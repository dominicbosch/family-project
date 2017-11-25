const fs = require('fs');
const glob = require('glob');
const express = require('express');
const app = express();

app.use('/', express.static(__dirname+'/detections'));

app.get('/getruns', (req, res) => {
	glob('detections/*.csv', (err, files) => {
		if (err) res.status(500).send(err.message); 
		else res.send(files.map(d => d.substr(11)));
	})
});

app.listen(8080, () => {
	console.log('Running on port 8080')
})