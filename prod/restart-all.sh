#!/bin/bash

./manage_celery.sh stop
wait

./fast_api_server.sh stop
wait

./clearlogs.sh
wait

./fast_api_server.sh start
wait

./manage_celery.sh start
wait