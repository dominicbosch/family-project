window.addEventListener('load', function() {
    showRuns();
});

function showRuns() {
    d3.json('getruns', function (data) {
        d3.select('#back').style('visibility', 'hidden');
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
            .on('click', im => {
                window.open(file.substr(0, file.length-4)+'_'+im.filename, '_blank')
            });
        head.append('td').text('Image');
        rows.append('td')
            .text(d => d.filename);
        head.append('td').text('Width');
        rows.append('td')
            .text(d => d.width);
        head.append('td').text('Height');
        rows.append('td')
            .text(d => d.height);
        head.append('td').text('Time');
        rows.append('td')
            .text(d => parseInt(d.time)+'ms');
        head.append('td').text('1st Classification');
        rows.append('td')
            .text(d => calcConf(d['1st class'], d['1st confidence']));
        head.append('td').text('2nd Classification');
        rows.append('td')
            .text(d => calcConf(d['2nd class'], d['2nd confidence']));
        console.log(csv);
    })
}

function calcConf(cls, d) {
    if (d === undefined) return '';
    return cls+' ('+parseInt(d*1000)/10+' %)';
}

function showImage(im) {
    
}