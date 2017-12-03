window.addEventListener('load', function() {
	console.log('LOADED');
	fetchData('http://'+window.location.host+'/logs')
		.then(listlog)
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
	document.querySelector('#temp td:nth-child(3)').innerHTML = data['DHT11-1'].temp;
	document.querySelector('#temp td:nth-child(4)').innerHTML = data['DHT11-2'].temp;
	document.querySelector('#humi td:nth-child(2)').innerHTML = data['AM2302'].humi;
	document.querySelector('#humi td:nth-child(3)').innerHTML = data['DHT11-1'].humi;
	document.querySelector('#humi td:nth-child(4)').innerHTML = data['DHT11-2'].humi;
}

const wd = ['So.', 'Mo.', 'Tue.', 'Wed.', 'Thur.', 'Fri.', 'Sat.'];

function listlog(data) {
    d3.select('#days').selectAll('option')
        .data(data).enter().append('option')
        .text(d => {
            let day = wd[new Date(data[i]).getDay()];
            return day+' '+d;
        })
        .change(d => console.log('change: ', d))
    
	console.log('comeon you lazy guy, implement the visualization', data);
}

// $.getJSON('https://www.highcharts.com/samples/data/jsonp.php?filename=usdeur.json&callback=?', function (data) {

//     Highcharts.chart('container', {
//         chart: {
//             zoomType: 'x'
//         },
//         title: {
//             text: 'USD to EUR exchange rate over time'
//         },
//         subtitle: {
//             text: document.ontouchstart === undefined ?
//                     'Click and drag in the plot area to zoom in' : 'Pinch the chart to zoom in'
//         },
//         xAxis: {
//             type: 'datetime'
//         },
//         yAxis: {
//             title: {
//                 text: 'Exchange rate'
//             }
//         },
//         legend: {
//             enabled: false
//         },
//         plotOptions: {
//             area: {
//                 fillColor: {
//                     linearGradient: {
//                         x1: 0,
//                         y1: 0,
//                         x2: 0,
//                         y2: 1
//                     },
//                     stops: [
//                         [0, Highcharts.getOptions().colors[0]],
//                         [1, Highcharts.Color(Highcharts.getOptions().colors[0]).setOpacity(0).get('rgba')]
//                     ]
//                 },
//                 marker: {
//                     radius: 2
//                 },
//                 lineWidth: 1,
//                 states: {
//                     hover: {
//                         lineWidth: 1
//                     }
//                 },
//                 threshold: null
//             }
//         },

//         series: [{
//             type: 'area',
//             name: 'USD to EUR',
//             data: data
//         }]
//     });
// });