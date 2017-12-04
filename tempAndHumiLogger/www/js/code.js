let formatHumi;
let formatTemp;
window.addEventListener('load', function() {
    let d3f = d3.format('.1f');
    formatTemp = d => d3f(d) + '°C';
    formatHumi = d => d3f(d) + '%';
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

let conf;
socket.onmessage = function (evt) {
    let obj = JSON.parse(evt.data);
    if (obj.conf) {
        conf = obj.conf;
        initTable();
    }
    if (obj.data) updateRealtimeMeasurements(obj.data);
};

socket.onerror = function (err) {
    console.error(err);
};

socket.onclose = function (evt) {
    console.log('socket closed', evt);
};

function initTable() {
    let sensors = conf.map(sensor => sensor.id);
    let titles = ['', 'Average'].concat(sensors);
    let d3El = d3.select('#status thead tr').selectAll('td').data(titles);
    d3El.enter().append('td')
        .merge(d3El).text(d => d);
    d3El.exit().remove();
}

function updateRealtimeMeasurements(data) {
    let wghts = conf.reduce((a, b) => ({ w: a.w+b.w })).w;
    let avgTemp = conf.map(s => data[s.id].temp * s.w).reduce((a, b) => a + b) / wghts;
    let avgHumi = conf.map(s => data[s.id].humi * s.w).reduce((a, b) => a + b) / wghts;
    
    let values = ['Temperature', avgTemp].concat(conf.map(s => data[s.id].temp));
    d3El = d3.select('#status tbody tr.temp').selectAll('td').data(values);
    d3El.enter().append('td')
        .merge(d3El).text((d, i) => i > 0 ? formatTemp(d) : d);
    d3El.exit().remove();

    values = ['Humidity', avgHumi].concat(conf.map(s => data[s.id].humi));
    d3El = d3.select('#status tbody tr.humi').selectAll('td').data(values);
    d3El.enter().append('td')
        .merge(d3El).text((d, i) => i > 0 ? formatHumi(d) : d);
    d3El.exit().remove();
}

const wd = ['So.', 'Mo.', 'Tue.', 'Wed.', 'Thur.', 'Fri.', 'Sat.'];

function listlog(data) {
    let sorted = data.sort((a, b) => {
        let arra = a.split('-');
        let arrb = b.split('-');
        if(parseInt(arra[0]) > parseInt(arrb[0])) return -1;
        if(parseInt(arra[0]) < parseInt(arrb[0])) return 1;
        if(parseInt(arra[1]) > parseInt(arrb[1])) return -1;
        if(parseInt(arra[1]) < parseInt(arrb[1])) return 1;
        if(parseInt(arra[2]) > parseInt(arrb[2])) return -1;
        if(parseInt(arra[2]) < parseInt(arrb[2])) return 1;
        return 0;
    });
    d3.select('#days')
        .on('change', requestDay)
        .selectAll('option')
        .data(sorted).enter().append('option')
        .attr('value', d => d)
        .text(d => {
            let day = wd[new Date(d).getDay()];
            return day+' '+d.split('-').reverse().join('.');
        });
    
    fetchData('http://'+window.location.host+'/log/'+sorted[0])
        .then(visualizeDay);
}

function requestDay() {
    let dat = d3.select('#days').property('value');
    fetchData('http://'+window.location.host+'/log/'+dat)
        .then(visualizeDay);
}

function visualizeDay(data) {
    let ds = [];
    for (let i = 0; i < data.length; i++) {
        let d = data[i];
        let dat = d.data.map(r => [parseInt(r[0]), parseFloat(r[1])]).sort((a, b) => b[0] - a[0]);
        // dat.pop();
        console.log(dat);
        ds.push({
            name: d.sensor.id+' - Temperature',
            data: dat
            // ,
            // color: {
            //     linearGradient: {
            //         x1: 0,
            //         y1: 0,
            //         x2: 0,
            //         y2: 1
            //     },
            //     stops: [
            //         [0, 'red'],
            //         [1, 'blue']
            //     ]
            // }
        })
        dat = d.data.map(r => [parseInt(r[0]), parseFloat(r[2])]).sort((a, b) => b[0] - a[0]);
        // dat.pop();
        console.log(dat);
        ds.push({
            name: d.sensor.id+' - Humidity',
            data: dat,
            yAxis: 1
        })
    }

    console.log(data);
    Highcharts.chart('container', {
        chart: {
            type: 'spline'
            ,
            zoomType: 'x'
        },
        title: {
            text: 'Temperature & Humidity Logger'
        },
        subtitle: {
            text: document.ontouchstart === undefined ?
                    'Click and drag in the plot area to zoom in' : 'Pinch the chart to zoom in'
        },
        xAxis: {
            type: 'datetime'
        },
        yAxis: [{
            title: {
                text: 'Temperature',
                style: {
                    color: Highcharts.getOptions().colors[2]
                }
            },
            labels: {
                format: '{value}°C',
                style: {
                    color: Highcharts.getOptions().colors[2]
                }
            },
            color: {
                linearGradient: {
                    x1: 0,
                    y1: 0,
                    x2: 0,
                    y2: 1
                },
                stops: [
                    [0, 'red'],
                    [1, 'blue']
                ]
            }
        },{
            gridLineWidth: 0,
            title: {
                text: 'Humidity',
                style: {
                    color: Highcharts.getOptions().colors[0]
                }
                
            },
            labels: {
                format: '{value}%',
                style: {
                    color: Highcharts.getOptions().colors[0]
                }
            },
            min: null,
            opposite: true
        }],
        legend: {
            enabled: false
        },
        plotOptions: {
            spline: {
                marker: {
                    radius: 1,
                    enabled: true
                }
            }
        },
        series: ds
    });
}
