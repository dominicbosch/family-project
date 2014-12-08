1. Remote Notification about Events
===================================

Get Device updates immediately without the need to use the UI. Alter server code:

- Possibility 1: in `automation/classes/AutomationController.js`

        AutomationController.prototype.updateNotification = function (id, object, callback) {
          /* alter here */
    
- Possibility 2 (prefer possibility 1...): in `automation/webserver.js`

        updateNotification: function (notificationId) {
              [ ... ]
              that.controller.updateNotification(notificationId, reqObj, function (notice) {
                    /* alter here */
      
2. Graph Theory
===============

Graphs have Edges e and Vertices v.
- v are the rooms (sensors). With attributes:
  - stay_time: average stay time (See Average below)
  - sensor: The sensor belonging to this edge ( we might have several edges per sensor because of single possible paths like when going from the kitchen to the office one will most likely always go through the stairs )
        
- e the possible transitions, i.e. the path through the house ( should the edges be directed? then edges need to be defined in both directions, so one way can differ from the other or even not exist). With attributes:
  - transition_time: how long are both lights on

Average:
 - [on-time]<sub>i</sub> = time from when turned on until turned off
 - [avg-on-time] = &mu; = sum ( [on-time]<sub>i</sub> ) / num-on-times [_&Nu;_]
 - [stddev-on-times] = &sigma; = sum( ( [on-time]<sub>i</sub> - &mu; )<sup>2</sup> ) / num-on-times [_&Nu;_]

![Average and Standard Deviation](http://upload.wikimedia.org/math/e/3/6/e36a4d7f54d0a78db9a26b0156f41555.png)
