window.addEventListener('load', function() {
    showRuns();
});

function showRuns() {
    d3.json('getruns', function (data) {
        console.log('runs', data)
        d3.selectAll('#content *').remove();
        d3.select('#content')
            .append('thead')
            .append('td')
            .text('Movidius Runs');
        let body = d3.select('#content').append('tbody');
        body.selectAll('tr')
            .data(data).enter()
            .append('tr')
            .on('click', showRun)
            .append('td')
            .text(d => d.substr(4, d.length-8));
    });
}

function showRun(file) {
    d3.select('#back').style('visibility', 'visible');
    d3.csv(file, (csv) => {
        d3.selectAll('#content *').remove();
        let head = d3.select('#content').append('thead');
        let body = d3.select('#content').append('tbody');
        let rows = body.selectAll('tr')
            .data(csv).enter()
            .append('tr')
            .on('click', showImage);
        head.append('td').text('Image');
        rows.append('td')
            .text(d => d.filename.substr(24));
        head.append('td').text('Time');
        rows.append('td')
            .text(d => parseInt(d.time)+'ms');
        head.append('td').text('1st Classification');
        rows.append('td')
            .text(d => d['1st class']);
        head.append('td').text('1st Confidence');
        rows.append('td')
            .text(d => calcConf(d['1st confidence']));
        head.append('td').text('2nd Classification');
        rows.append('td')
            .text(d => d['2nd class']);
        head.append('td').text('2nd Confidence');
        rows.append('td')
            .text(d => calcConf(d['2nd confidence']));
        console.log(csv);
    })
}

function calcConf(d) {
    if (d === undefined) return '';
    return parseInt(d*1000)/10+' %';
}

function showImage(im) {
    window.open(im.filename, '_blank');
}