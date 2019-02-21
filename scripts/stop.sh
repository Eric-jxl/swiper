#!/bin/bash

PROJECT_DIR='/opt/swiper'
PIDFILE="$PROJECT_DIR/logs/gunicorn.pid"

kill `cat $PIDFILE`
