document.addEventListener('DOMContentLoaded', function() {
	function addListeners(img, src) {
		img.on('mouseover', function() {
			console.log('mouseover', src);
			d3.select('#bigpic').attr('src','thumbs/'+src);
		})
		.on('mouseout', function() {
			d3.select('#bigpic').attr('src', null);
		});
	}
	d3.json('log.json', function(err, data) {
		var x = d3.scaleLinear()
			.domain([data.tsmin, data.tsmax])
			.range([0, 100]);
		if(err) console.error(err);
		else {
			console.log(data);
			for (let i = 0; i < data.snapshots.length; i++) {
				let fc = data.snapshots[i];
				let img = d3.select('#snaps')
					.append('div')
					.style('left', x(fc.ts)+'%')
					.append('img')
						.attr('src', 'thumbs/'+fc.img)
						.classed('snapshot', true);
				addListeners(img, fc.img);
			}
			for (let i = 0; i < data.faces.length; i++) {
				let fc = data.faces[i];
				d3.select('#photos')
					.append('div')
					.style('left', x(fc.ts)+'%')
					.append('img')
						.attr('src', 'img/photo.png')
						.classed('photo', true);
				let img = d3.select('#faces')
					.append('div')
					.style('left', x(fc.ts)+'%')
					.append('img')
						.attr('src', 'thumbs/'+fc.img)
						.classed('face', true);
				addListeners(img, fc.img);
			}

			// steering int
			// speed int
			// ultrasonic int
			// camerafps int
			// detectfps int
			for (let i = 0; i < data.facedetect.length; i++) {
				let fc = data.facedetect[i];
				let img = d3.select('#arrows')
					.append('div')
					.style('left', x(fc.ts)+'%')
					.append('img')
						.attr('src', 'img/arrow-blue.png')
						.style('transform', 'rotate('+(270+90*fc.val)+'deg)')
						.classed('arrow', true);
			}
			// motorstate str
			console.log(data.motorstate);
		}
	});
});