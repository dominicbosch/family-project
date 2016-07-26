#! /bin/sh
### BEGIN INIT INFO
# Provides:		  [YOUR APPLICATION]
# Required-Start:	
# Required-Stop:	 
# Default-Start:	 2 3 4 5
# Default-Stop:	  0 1 6
# Short-Description: [YOUR APPLICATION] does stuff
# Description:	   Start [YOUR APPLICATION]
### END INIT INFO

# Description: [YOUR APPLICATION] does a lot of stuff
# Author: Dominic Bosch <dominic.bosch.db@gmail.com>

PATH=/bin:/usr/bin:/sbin:/usr/sbin
NAME=[YOUR APPLICATION]
DAEMON_PATH=/opt/[YOUR APPLICATION]
PIDFILE=/var/run/$NAME.pid

case "$1" in
  start)
	echo -n "Starting [YOUR APPLICATION]: "
	start-stop-daemon --start  --pidfile $PIDFILE --make-pidfile  --background --no-close --chdir $DAEMON_PATH --exec $NAME > /dev/null 2>&1
	echo "done."
	;;
  stop)
	echo -n "Stopping [YOUR APPLICATION]: "
	start-stop-daemon --stop --quiet --pidfile $PIDFILE
	rm $PIDFILE
	echo "done."
	;;
  restart)
	echo "Restarting [YOUR APPLICATION]: "
	sh $0 stop
	sleep 10
	sh $0 start
	;;
  *)
	echo "Usage: /etc/init.d/[YOUR APPLICATION] {start|stop|restart}"
	exit 1
	;;
esac
exit 0