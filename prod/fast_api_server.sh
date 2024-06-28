#!/bin/bash

FASTAPI_APP="main:app"
LOGFILE="fastapi.log"
PIDFILE="fastapi_server.pid"
HOST="0.0.0.0"
PORT="443"
SSL_KEYFILE="/home/trainboxai/backend/rippo/certs/privkey.pem"
SSL_CERTFILE="/home/trainboxai/backend/rippo/certs/fullchain.pem"

start_fastapi() {
    echo "Starting FastAPI server..."
    nohup authbind uvicorn $FASTAPI_APP --host $HOST --port $PORT --ssl-keyfile $SSL_KEYFILE --ssl-certfile $SSL_CERTFILE > $LOGFILE 2>&1 &
    echo $! > $PIDFILE
    echo "FastAPI server started."
}

stop_fastapi() {
    if [ -f $PIDFILE ]; then
        echo "Stopping FastAPI server..."
        kill -TERM $(cat $PIDFILE)
        rm -f $PIDFILE
        echo "FastAPI server stopped."
    else
        echo "No PID file found. FastAPI server might not be running."
    fi
}

restart_fastapi() {
    stop_fastapi
    start_fastapi
}

status_fastapi() {
    if [ -f $PIDFILE ]; then
        if ps -p $(cat $PIDFILE) > /dev/null; then
            echo "FastAPI server is running with PID $(cat $PIDFILE)."
        else
            echo "PID file found but FastAPI server is not running."
        fi
    else
        echo "No PID file found. FastAPI server is not running."
    fi
}

case "$1" in
    start)
        start_fastapi
        ;;
    stop)
        stop_fastapi
        ;;
    restart)
        restart_fastapi
        ;;
    status)
        status_fastapi
        ;;
    *)
        echo "Usage: $0 {start|stop|restart|status}"
        exit 1
        ;;
esac