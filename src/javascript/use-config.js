var fs = require( 'fs' ),
  request = require( 'request' ),
  baseUrl = 'http://192.168.0.79:8083/JS/Run/zway.',
  arrArgs = process.argv.splice( 2 ),
  fGetDeviceFunction, fParseDeviceFunction;

if( arrArgs < 2 ) {
  console.log( 'Provide a device ID and a function to execute!' );
  return; 
}

fGetDeviceFunction = function( err, data ) {
  var oConfig, oDevice, oFunction;
  try {
    oConfig = JSON.parse( data );
  } catch( e ) {
    console.log( 'Error parsing config file!' );
  }
  console.log( 'Done loading data!' );

  oDevice = oConfig[ arrArgs[ 0 ] ];
  if( !oDevice ) {
    console.log( 'Invalid device: "' + arrArgs[ 0 ] + '"!' );
    return;
  }

  oFunction = oDevice.functions[ arrArgs[ 1 ] ];
  if( !oFunction ) {
    console.log( 'Invalid function: "' + arrArgs[ 1 ] + '"!' );
    return;
  }

  fParseDeviceFunction( oDevice.device, oFunction );
};

fParseDeviceFunction = function( device, oFunction ) {
  var reqUrl,
      cmd = oFunction.command;
  if( cmd.indexOf( "%arg%" ) > 0 ) {
    if( !arrArgs[ 2 ] ) {
      console.log( 'Please supply an argument to this function!' );
      return;
    }
    cmd = cmd.replace( '%arg%', arrArgs[ 2 ] );
  }
  reqUrl = baseUrl + 'devices[' + device
    + '].instances[' + oFunction.instance
    + '].commandClasses[' + oFunction.commandClass
    + ']' + cmd;
    console.log(reqUrl);
  request( reqUrl, function( err, resp, body ) {
    console.log( body );
  });

};

fs.readFile( '../config/devices.json', 'utf-8', fGetDeviceFunction);