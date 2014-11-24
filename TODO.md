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
      
