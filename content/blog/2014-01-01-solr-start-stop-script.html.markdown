Title: Solr Start/Stop Script
Date: 2014-01-01 16:20 EST
Tags: Solr, Linux
Summary: This took a while to sort out, and I ended up more or less copying the script for NGINX.

At some point I'm going to write a much longer post on how to set up Solr on Linux, but for now
here's a start/stop script that works well.

```sh
#!/bin/sh

### BEGIN INIT INFO
# Provides:             solr
# Short-Description:    starts the solr server
# Description:          starts solr using start-stop-daemon
### END INIT INFO

SOLR_DIR="/opt/solr/django"  # Change to your own solr directory!
PID="/run/solr/solr.pid"
USER="solr"
DAEMON="/usr/bin/java"
DAEMON_ARGS="-server $JAVA_OPTS -Dsolr.solr.home=$SOLR_DIR/multicore -jar start.jar"
NAME="solr"
DESC="solr"

# Include solr configuration defaults if available
if [ -f /etc/default/solr ]; then
    . /etc/default/solr
fi

test -x $DAEMON || exit 0

set -e

. /lib/lsb/init-functions

start() {
    start-stop-daemon --start --quiet --pidfile $PID --make-pidfile \
        --chdir $SOLR_DIR --chuid $USER \
        --background --retry 5 --exec $DAEMON -- $DAEMON_ARGS
}

stop() {
    start-stop-daemon --stop --quiet --pidfile $PID --retry 5
}

case "$1" in
    start)
        log_daemon_msg "Starting $DESC" "$NAME"
        start
        log_end_msg $?
        ;;
    stop)
        log_daemon_msg "Stopping $DESC" "$NAME"
        stop
        log_end_msg $?
        ;;
    restart)
        log_daemon_msg "Restarting $DESC" "$NAME"
        stop
        sleep 3
        start
        log_end_msg $?
        ;;
    status)
        status_of_proc -p $PID "$DAEMON" java
        ;;
    *)
        echo "Usage: $NAME {start|stop|restart|status}" >&2
        exit 1
        ;;
esac

exit 0
```
