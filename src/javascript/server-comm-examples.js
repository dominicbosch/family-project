var fCallback, fCheckSensors,
	arrSensorIds = [],
	fs = require( 'fs' ),
	http = require( 'http' ),
	baseUrl = 'http://192.168.0.79:8083/JS/Run/zway.';

// [2].instances[0].commandClasses[37].Set(0)

// A helper function which grabs all data from a server response and packs it in the data string
fFetchServerAnswer = function( url, callbackFunc ) {
	http.get( url, function( response ) {
		var data = ''; // data will be temporaily stored here

		response.on( 'data', function( chunk ) { // if we receive a chunk of data we append it to data
			data += chunk;
		});

		response.on( 'end', function () { // If the server response ended we can process the data
			callbackFunc( data ); // Pass the data to the callback function if ready
		});
	});
};


fCheckSensors = function() {
	for( var i = 0; i < arrSensorIds.length; i++ ) {
		console.log('updateing sensor ' + arrSensorIds[ i ])
		fUpdateSensor( arrSensorIds[ i ] );
	};
	setTimeout( fCheckSensors, 2 * 60 * 1000 );
};

fUpdateSensor = function( sensorID ) {
	// Force a sensor update: (really needed?)

	//FIXME somehow the server gets too busy here and drops packages or whatever tcp error happens
	http.get( baseUrl + 'devices[' + sensorID + '].instances[0].commandClasses[37].Get()', function() {
		// Maybe it will be fixed if we only ask the status after letting the raspberry update
		fFetchServerAnswer( baseUrl + 'devices[' + sensorID + '].instances[0].commandClasses[37].data.level', function( data ) {
			console.log( sensorID + ": " );
			console.log( data );
		});
	});
}

fFetchServerAnswer( baseUrl + 'devices', function( data ) {
	var oSensors = JSON.parse( data );

	for( var el in oSensors ) {
		arrSensorIds.push( el );
	}
	fCheckSensors(); // Start the sensor status check
});
// fs.appendFile( 'sensor-data.json', JSON.stringify( ob, null, 2 )); 

// {
// 	timestamp: '17:03',
// 	devices: {
// 		'0': true,
// 		'1': false,
// 		'2': true
// 	}
// } 



