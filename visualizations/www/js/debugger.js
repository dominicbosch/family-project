document.addEventListener('DOMContentLoaded', function() {
	d3.json('log.json', function(err, data) {
		if(err) console.error(err);
		else {
			console.log(data);
		}
	});
});