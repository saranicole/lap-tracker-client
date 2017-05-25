#!/usr/bin/env bash
pidfile=/var/run/face_publisher.pid
if [ -e $pidfile ]; then
kill -9 `cat /var/run/$pidfile`
rm $pidfile
fi
