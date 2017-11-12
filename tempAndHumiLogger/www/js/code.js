window.addEventListener('load', function() {
	console.log('LOADED');
	fetchData('http://'+window.location.host+'/getlogs')
		.then(visualizeLog)
		.catch((err) => console.error('Couldn\'t get log: '+err.message));
});

function fetchData(url) {
	return new Promise(function(resolve, reject) {
		// Yay let's do it the real way!
		let xhr = new XMLHttpRequest();
		xhr.onreadystatechange = function() {
			if (xhr.readyState === XMLHttpRequest.DONE) {
				if (xhr.status === 200) {
					resolve(JSON.parse(xhr.responseText));
				} else {
					reject(new Error(xhr.status));
				}
			}
		};
		xhr.open('GET', url, true);
		xhr.send();
	});
}

let socket = new WebSocket('ws://'+window.location.host);
console.log('Connecting socket to '+'ws://'+window.location.host)

socket.onmessage = function (event) {
	console.log('realtime measurement', event.data);
	updateRealtimeMeasurements(JSON.parse(event.data));
};

socket.onerror = function (err) {
	console.error(err);
};

socket.onclose = function (evt) {
	console.log('socket closed', evt);
};

function updateRealtimeMeasurements(data) {
	document.querySelector('#temp td:nth-child(2)').innerHTML = data['AM2302'].temp;
	document.querySelector('#temp td:nth-child(3)').innerHTML = data['DHT11 #1'].temp;
	document.querySelector('#temp td:nth-child(4)').innerHTML = data['DHT11 #2'].temp;
	document.querySelector('#humi td:nth-child(2)').innerHTML = data['AM2302'].humi;
	document.querySelector('#humi td:nth-child(3)').innerHTML = data['DHT11 #1'].humi;
	document.querySelector('#humi td:nth-child(4)').innerHTML = data['DHT11 #2'].humi;
}



function visualizeLog(data) {
	console.log('comeon you lazy guy, implement the visualization', data);
}
