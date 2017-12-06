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
    let titles = ['', 'wAverage'].concat(sensors);
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

let isGrouped = true;
function toggleGrouping() {
    isGrouped = !isGrouped;
    d3.select('#grping').text(isGrouped ? 'Show all Sensors' : 'Show wAverage');
    requestDay();
}

let groupingUnits = [[
    'week',                         // unit name
    [1]                             // allowed multiples
], [
    'month',
    [1, 2, 3, 4, 6]
]];
let groupingBase = 3;
function convertSeries(ds, idVal) {
    let series = [];
    let totTime = 0;
    let totVal = 0;
    let j;
    let d = ds.data;
    // make aggregation dependent on trust (weight of sensor)
    let an = Math.floor(groupingBase / ds.sensor.w);
    for (j = 0; j < d.length-1; j++) {
        totTime += parseInt(d[j][0]);
        totVal += parseFloat(d[j][idVal]);
        if (j % an === an-1) {
            series.push([Math.floor(totTime/an), totVal/an]);
            totTime = 0;
            totVal = 0;
        }
    }
    let n = j % an;
    series.push([Math.floor(totTime/n), totVal/n]);
    series.sort((a, b) => a[0]-b[0]);
    return series;
}

function groupData(data) {
    // make aggregation dependent on trust (weight of sensor)
    let tw = 0;
    for (let i = 0; i < data.length; i++) {
        tw += data[i].sensor.w;
    }
    let an = Math.floor(groupingBase / (tw / data.length));
    let arrTemp = [];
    let arrHumi = [];
    let totTime = 0;
    let totTemp = 0;
    let totHumi = 0;
    let i;

    // we crawl through the first data set as a reference (at least the first needs to exist)
    for (i = 0; i < data[0].data.length - 2; i++) {
        // since we have same number of measurements for each sensor we can just aggregate them
        for (let j = 0; j < data.length; j++) {
            let w = data[j].sensor.w;
            totTime += parseInt(data[j].data[i][0]) * w;
            totTemp += parseFloat(data[j].data[i][1]) * w;
            totHumi += parseFloat(data[j].data[i][2]) * w;
        }
        if (i % an === an-1) {
            arrTemp.push([Math.floor(totTime/an/tw), totTemp/an/tw]);
            arrHumi.push([Math.floor(totTime/an/tw), totHumi/an/tw]);
            totTime = 0;
            totTemp = 0;
            totHumi = 0;
        }
    }
    let n = i % an;
    console.log('done:', totTime, totTemp, totHumi);
    arrTemp.push([Math.floor(totTime/n/tw), totTemp/n/tw]);
    arrHumi.push([Math.floor(totTime/n/tw), totHumi/n/tw]);
    arrTemp.sort((a, b) => a[0]-b[0]);
    arrHumi.sort((a, b) => a[0]-b[0]);
    console.log(arrTemp, arrHumi);

    return [{
        name: 'wAverage - Temperature',
        color: 'hsl(340, 70%, 70%)', 
        data: arrTemp
    },
    {
        name: 'wAverage - Humidity',
        color: 'hsl(210, 70%, 70%)', 
        data: arrHumi,
        yAxis: 1
    }];
}

function visualizeDay(data) {
    let ds = [];
    if(isGrouped) ds = groupData(data);
    else {
        for (let i = 0; i < data.length; i++) {
            ds.push({
                name: data[i].sensor.id+' - Temperature',
                color: 'hsl(340, 80%, '+(60+10*i)+'%)', 
                data: convertSeries(data[i], 1)
            })
            ds.push({
                name: data[i].sensor.id+' - Humidity',
                color: 'hsl(210, 50%, '+(60+10*i)+'%)', 
                data: convertSeries(data[i], 2),
                yAxis: 1
            })
        }
    }

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
                    color: 'hsl(340, 80%, 50%)'
                }
            },
            labels: {
                format: '{value}°C',
                style: {
                    color: 'hsl(340, 80%, 50%)'
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
            },
            min: 16,
            max: 23
        },{
            gridLineWidth: 0,
            title: {
                text: 'Humidity',
                style: {
                    color: 'hsl(210, 50%, 50%)'
                }
            },
            labels: {
                format: '{value}%',
                style: {
                    color: 'hsl(210, 50%, 50%)'
                }
            },
            min: 40,
            max: 56,
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
