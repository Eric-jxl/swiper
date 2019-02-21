#!/bin/bash

PROJECT_DIR='/opt/swiper'
PIDFILE="$PROJECT_DIR/logs/gunicorn.pid"

# 简单粗暴，但是有效
# $PROJECT_DIR/scripts/stop.sh
# $PROJECT_DIR/scripts/start.sh

# 平滑重启
kill -HUP `cat $PIDFILE`
