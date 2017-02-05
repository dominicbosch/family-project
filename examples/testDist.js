var usonic = require('r-pi-usonic');

usonic.init(function (error) {
    if (error) {
        console.log('Error');
    } else {
        console.log('No Error');
    }
});

var sensor = usonic.createSensor(+7, 23, 450);

var distance = sensor();

console.log(distance);
