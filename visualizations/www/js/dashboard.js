window.addEventListener('load', function load(event){
	window.removeEventListener('load', load, false);


	var socket = io.connect('http://'+window.location.hostname+':8080');
	var df = d3.format('.2');
	function fVal(val) {
		// since currently we receive values between [0,1), we transform them 
		// to have the range [-1, 1), and then format them to two point precision
		return df((val-0.5)*2);
	}
	// we received an accelerator measurement over the socket from the server
	socket.on('measurement', function (data) {
		console.log('Got measurement', data);

		// we update the arrow tip position
		d3.select('#arrow')
			.attr('x2', data.x*200)
			.attr('y2', data.y*200);
		
		// we add the new point to the path that shows the arrow history
		var d = d3.select('#xypath').attr('d');
		d3.select('#xypath').attr('d', d+' L '+data.x*200+' '+data.y*200);
		
		// we also need to update the text label with the new values
		d3.select('#xyval')
			.attr('x', data.x*200+(Math.sign(data.x-0.5)*20))
			.attr('y', data.y*200+(Math.sign(data.y-0.5)*20))
			.text('('+fVal(data.x)+','+fVal(data.y)+')');



		// Z is a bit more complicated because it is not allowed to have negative heights
		var zdir = Math.sign(data.z-0.5);
		var zsize = zdir*(data.z-0.5)*200;

		// the size is set as simple as for x/y on the arrow
		d3.select('#zrect')
			.attr('height', zsize);

		// the y position depends on whether we are in the positive or negative range
		if(zdir > 0) {
			d3.select('#zrect')
				.attr('y', 100);
		} else {
			d3.select('#zrect')
				.attr('y', 100-zsize);
		}
		// at  last we also update the text label for Z with the new values
		d3.select('#zval')
			.attr('y', data.z*200+(zdir*10))
			.text(fVal(data.z));
	});

	// we receive a command over the socket and write it into the div tag with ID "currentcommand"
	socket.on('currentcommand', function (data) {
		d3.select('#currentcommand').text(data.cmd);
	});

	d3.select('#starter').on('click', function() {
		if(d3.select('#starter').classed('stopped')) {
			socket.emit('engine-start');
		} else {
			socket.emit('engine-stop');
		}
	});

	socket.on('engine-started', function() {
		d3.select('#starter')
			.classed('started', true)
			.classed('stopped', false);
	});

	socket.on('engine-stopped', function() {
		d3.select('#starter')
			.classed('started', false)
			.classed('stopped', true);
	});

	socket.on('steer', function(val) {
		d3.select('#wheel')
			.transition()
			.duration(500)
			.style('transform', 'rotate('+val+'deg)');
	});


	// 	io.emit('ultrasonic', parseFloat(extractValue(line, strng, 2)));

	// } else if(line.indexOf(strng='obstc | Cleared obstacle counter') > -1) {
	// 	io.emit('ultrasonic', -1);


	// // temperature
	// } else if(line.indexOf(strng='sensr | Temperature: ') > -1) {
	// 	io.emit('temperature', parseFloat(extractValue(line, strng, 2)));
		

	// // accelerator X axis
	// } else if(line.indexOf(strng='sensr | Accelerator: X=') > -1) {
	// 	io.emit('accelerator-x', parseFloat(extractValue(line, strng, 0)));
		

	// // accelerator Y axis
	// } else if(line.indexOf(strng='sensr | Accelerator: Y=') > -1) {
	// 	io.emit('accelerator-y', parseFloat(extractValue(line, strng, 0)));
		

	// // accelerator Z axis
	// } else if(line.indexOf(strng='sensr | Accelerator: Z=') > -1) {
	// 	io.emit('accelerator-z', parseFloat(extractValue(line, strng, 0)));
		
		
	// // Speed
	// } else if(line.indexOf(strng='MOTOR | FINAL DECISION SENT: ') > -1) {
	// 	io.emit('motor', parseInt(extractValue(line, strng, 0)));

	// } else if(line.indexOf(strng='motor | ') > -1) {
	// 	io.emit('motor-status', extractValue(line, strng, 0));

		
	// // face detection
	// } else if(line.indexOf('faces | new face(s) detected ') > -1) {
	// 	strng = ', nearest at ';
	// 	io.emit('steer', parseFloat(extractValue(line, strng, 1)));
		
	// } else if(line.indexOf(strng='steer | Heading straight') > -1) {
	// 	io.emit('steer', 0);

	var timer;
	var lastFaceDetected;
	var cam = document.getElementById('camera');
	socket.on('faceCapture', function(img) {
		lastFaceDetected = (new Date()).getTime();
		cam.setAttribute('src', 'data:image/jpg;base64,'+img);
		if(!timer) {
			timer = setInterval(function() {
				var now = (new Date()).getTime();
				var elapsed = Math.round((now-lastFaceDetected)/10);
				d3.select('#elapsed').text((elapsed/100)+'s since face detection');
			}, 1000/11);
		} 
	});

	// The user pressed the send button and wants to send a command to the server
	function sendCommand() {
		// if the socket is ready we try to send the command from the input box,
		if(socket) {
			var val = document.getElementById('cmd').value;
			complexDataObject.commandValue = val;
			
			console.log('Sending event to server: ', complexDataObject);
			socket.emit('command', complexDataObject);
		}
	}


},false);