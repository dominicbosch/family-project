document.addEventListener('DOMContentLoaded', function() {
	d3.json('log.json', function(err, data) {
		var x = d3.scaleLinear()
			.domain([data.tsmin, data.tsmax])
			.range([0, 100]);
		if(err) console.error(err);
		else {
			console.log(data);
			for (let i = 0; i < data.snapshots.length; i++) {
				let fc = data.snapshots[i];
				d3.select('#thumbs')
					.append('div')
					.style('left', x(fc.ts)+'%')
					.append('img')
						.attr('src', 'thumbs/'+data.snapshots[i].img)
						.classed('snapshot', true);
			}
			for (let i = 0; i < data.faces.length; i++) {
				let fc = data.faces[i];
				d3.select('#thumbs')
					.append('div')
					.style('left', x(fc.ts)+'%')
					.append('img')
						.attr('src', 'thumbs/'+fc.img)
						.classed('face', true);
				d3.select('#thumbs')
					.append('div')
					.style('left', x(fc.ts)+'%')
					.append('img')
						.attr('src', 'img/photo.png')
						.classed('photo', true);
			}
		}
	});
});