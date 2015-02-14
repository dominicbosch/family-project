
/*
 * EventForwarding is our first extension to the z-way server which allows
 * for the real-time reactivity for other systems
 * TODO: dynamic callback Url registration
 */
console.log('EVENTHANDLER STARTED');
var writeLog, sendMessageToRemoteHost;//,
//    fs = require.nodeRequire( 'fs' );

function EventForwarding ( id, controller ) {
  EventForwarding.super_.call(this, id, controller); // Call superconstructor first ( AutomationModule )

    this.controller = controller;
};

inherits( EventForwarding, AutomationModule );
_module = EventForwarding;

writeLog = function( str ) {
console.log("EH: " + str);
  //fs.appendFile( 'log.txt', str );
};

sendMessageToRemoteHost = function( payload ) {
console.log('sending something over EventHandler');
  http.request({
    url: '192.168.0.79:8888/eventlistener',
    method: 'POST',
    data: payload,
    success: function( response ) {
      writeLog( 'Successfully forwarded event:' );
      writeLog( JSON.stringify( payload ) );
    },
    error: function( response ) {
      writeLog( 'Error during forwarding request: ' + response.statusText );
    } 
  });
};

EventForwarding.prototype.init = function( config ) {
  var fFilteredListUpdate, fDeviceUpdate;
var fWrite = function(source){return function(){
console.log('EVENT YAY! ' + source)};};
this.controller.on('device.metricUpdated', fWrite('device.metricUpdated'));
this.controller.on('change:metrics:level', fWrite('change:metrics:level'));
this.controller.on('sensorsPolling.poll', fWrite('sensorPolling.poll'));
this.controller.on('ZWaveGate.dataBind', fWrite('ZWaveGate.dataBind'));
this.controller.on('all', fWrite('all'));
this.controller.on('change', fWrite('change'));


/*    console.log('EH INIT!');
    console.log(this.config.device);
    console.log(this.controller.devices);
    console.log(this.controller.devices.get(this.config.device));
*/

  this.controller.devices.each(function( el ) {
el.on('all', fWrite('on all in each el'+JSON.stringify(el))); // bei button click, aber nur switches!?
el.on('change', fWrite('on change in each el'+JSON.stringify(el))); // bei button click, aber nur switches!?
});
  
/* Try filtered (for switches) list update and result */
  this.controller.devices.filter(function( el ) {
console.log('filtering device list:', JSON.stringify(el));
    return el.get( 'deviceType' ) === 'switchBinary';
  }).map(function( el ) {
    el.on( 'change:metrics', sendMessageToRemoteHost );
  });

  /* try general device listener */
  this.controller.on('device.metricUpdated', function( vdevId, name, value ) {
    var dev = self.controller.devices.get( vdevId );
console.log(vdevId + " : " + name + " : " + value);
    sendMessageToRemoteHost({
      deviceId: vdevId,
      name: name,
      value: value,
      metrics: dev.get( 'metrics' )
    });
  });
};


/* Useful features: */


// EventForwarding.prototype.stop = function () {
//     // Handle stop?
// };


// fs = require.nodeRequire('fs');


// http.request({
//     url: url,
//     method: this.config.method,
//     async: true,
//     success: function(response) {
//         var data = typeof(response.data) == 'object' ? '(' + JSON.stringify(response.data) + ')': response.data.toString();
//         vDev.set('metrics:level', parser ? eval(parser.replace(/%%/g, data)) : response.data);
//     },
//     error: function(response) {
//         console.log('Can not make request: ' + response.statusText); // don't add it to notifications, since it will fill all the notifcations on error
//     } 
// });
