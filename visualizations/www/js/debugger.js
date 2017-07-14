let data;
let d3Graph;
let xScale;
let xAxis;
let yAxis;
let d3Steer;
let d3Speed;
let d3Ultrasonic;
let formatPrct = d3.format('.0%');

document.addEventListener('DOMContentLoaded', function() {
	d3Graph = d3.select('#graph');
	d3.select('body').on('mousemove', function() {
		let ts = xScale.invert(d3.event.clientX);
		let val;
		d3.select('#timeline').style('left', d3.event.clientX+'px');
		
		val = getLastVal(data.camerafps, ts);
		d3.select('#ttcamerafps .val').text((val||0).toFixed(2));
		
		val = getLastVal(data.detectfps, ts);
		d3.select('#ttdetectfps .val').text((val||0).toFixed(2));
		
		val = getLastVal(data.facedetect, ts);
		d3.select('#ttface .val').text(formatPrct(val||0));

		val = getLastVal(data.steering, ts);
		d3.select('#ttsteer .val').text(formatPrct(val||0));

		val = getLastVal(data.motorstate, ts);
		d3.select('#ttmotorstate .val').text(val||'');

		val = getLastVal(data.speed, ts);
		d3.select('#ttspeed .val').text(formatPrct(val||0));

		let arr = data.faces.concat(data.snapshots).sort(function(a, b) { return a.ts-b.ts });
		val = getLastVal(arr, ts);
		if(val) d3.select('#bigpic').attr('src', 'thumbs/'+val);
		else d3.select('#bigpic').attr('src', null);

		val = getLastVal(data.ultrasonic, ts);
		d3.select('#ttultrasonic .val').text((val||0).toFixed(2)+'m');

	});
	d3.json('log.json', function(err, data) {
		if(err) console.error(err);
		else addVisualizations(data);
	});
});

function addVisualizations(d) {
	console.log(d);
	data = d;
	updateWidth();

	let xPrct = d3.scaleLinear()
		.domain([data.tsmin, data.tsmax])
		.range([0, 100]);

	xScale = d3.scaleLinear()
		.domain([data.tsmin, data.tsmax])
		.range([40, width]);

	yScale = d3.scaleLinear()
		.domain([-1, 1])
		.range([390, 10]);

	d3Graph.append('text')
		.attr('class', 'timestamp')
		.attr('x', 45)
		.attr('y', 395)
		.text('Measurement started: '+d3.timeFormat('%d.%m.%Y %H:%M:%S.%L')(data.tsmin));

	xAxis = d3.axisBottom(xScale)
		.tickFormat(d3.timeFormat('%H:%M:%S'))
		.ticks(5)
		.tickSizeOuter(0);
	d3Graph.append('g')
		.attr('class', 'axis xaxis')
		.call(xAxis);

	yAxis = d3.axisLeft(yScale)
		.tickFormat(formatPrct)
		.ticks(5);
	d3Graph.append('g')
		.attr('class', 'axis yaxis')
		.call(yAxis);

	for (let i = 0; i < data.snapshots.length; i++) {
		let fc = data.snapshots[i];
		let img = d3.select('#snaps')
			.append('div')
			.style('left', xPrct(fc.ts)+'%')
			.append('img')
				.attr('src', 'thumbs/'+fc.img)
				.classed('snapshot', true);
		// addListeners(img, fc.img);
	}
	for (let i = 0; i < data.faces.length; i++) {
		let fc = data.faces[i];
		d3.select('#photos')
			.append('div')
			.style('left', xPrct(fc.ts)+'%')
			.append('img')
				.attr('src', 'img/photo.png')
				.classed('photo', true);
		let img = d3.select('#faces')
			.append('div')
			.style('left', xPrct(fc.ts)+'%')
			.append('img')
				.attr('src', 'thumbs/'+fc.img)
				.classed('face', true);
		// addListeners(img, fc.img);
	}
	for (let i = 0; i < data.facedetect.length; i++) {
		let fc = data.facedetect[i];
		let img = d3.select('#arrows')
			.append('div')
			.style('left', xPrct(fc.ts)+'%')
			.append('img')
				.attr('src', 'img/arrow-blue.png')
				.style('transform', 'rotate('+(270+90*fc.val)+'deg)')
				.classed('arrow', true);
	}

	d3Steer = d3Graph.append('g').attr('class', 'steer');
	d3Steer.selectAll('circle').data(data.steering).enter()
		.append('circle').attr('r', 3).attr('cy', function(d) { return yScale(d.val) })
	d3Speed = d3Graph.append('g').attr('class', 'speed');
	d3Speed.selectAll('circle').data(data.speed).enter()
		.append('circle').attr('r', 2).attr('cy', function(d) { return yScale(d.val) })
	d3Ultrasonic = d3Graph.append('g').attr('class', 'ultrasonic');
	d3Ultrasonic.selectAll('circle').data(data.ultrasonic).enter()
		.append('circle').attr('r', 1).attr('cy', function(d) { return yScale(d.val/2) })

	// camerafps int
	// detectfps int
	// motorstate str
	console.log(data.motorstate);
	updateVisualization();
}
function getLastVal(arr, ts) {
	let i = 0;
	while(arr[i] && arr[i].ts < ts) i++;
	if(arr[i-1] !== undefined) return arr[i-1].val || arr[i-1].img; 
	else return null;
}
// function addListeners(img, src) {
// 	img.on('mouseover', function() {
// 		console.log('mouseover', src);
// 		d3.select('#bigpic').attr('src','thumbs/'+src);
// 	})
// 	.on('mouseout', function() {
// 		d3.select('#bigpic').attr('src', null);
// 	});
// }

let width = 0;
window.addEventListener('resize', updateVisualization, true);
function updateWidth() {
	width = parseInt(d3Graph.style('width').slice(0, -2));
}
function updateVisualization() {
	updateWidth();
	if(width > 500) xAxis.ticks(6);
	else xAxis.ticks(3);

	xScale.range([40, width]);
	d3Graph.select('.xaxis')
		.call(xAxis);

	d3Steer.selectAll('circle').attr('cx', function(d) { return xScale(d.ts) })
	d3Speed.selectAll('circle').attr('cx', function(d) { return xScale(d.ts) })
	d3Ultrasonic.selectAll('circle').attr('cx', function(d) { return xScale(d.ts) })
}