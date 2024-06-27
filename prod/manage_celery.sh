#!/bin/bash

CELERY_APP="celery_app"
LOGFILE="celery.log"
PIDFILE="celery_worker.pid"

start_celery() {
    echo "Starting Celery worker..."
    celery -A $CELERY_APP worker --loglevel=debug --logfile=$LOGFILE --pidfile=$PIDFILE &
    echo "Celery worker started."
}

stop_celery() {
    if [ -f $PIDFILE ]; then
        echo "Stopping Celery worker..."
        kill -TERM $(cat $PIDFILE)
        rm -f $PIDFILE
        echo "Celery worker stopped."
    else
        echo "No PID file found. Celery worker might not be running."
    fi
}

restart_celery() {
    stop_celery
    start_celery
}

status_celery() {
    if [ -f $PIDFILE ]; then
        if ps -p $(cat $PIDFILE) > /dev/null; then
            echo "Celery worker is running with PID $(cat $PIDFILE)."
        else
            echo "PID file found but Celery worker is not running."
        fi
    else
        echo "No PID file found. Celery worker is not running."
    fi
}

case "$1" in
    start)
        start_celery
        ;;
    stop)
        stop_celery
        ;;
    restart)
        restart_celery
        ;;
    status)
        status_celery
        ;;
    *)
        echo "Usage: $0 {start|stop|restart|status}"
        exit 1
        ;;
esac