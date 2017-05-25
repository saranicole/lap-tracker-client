#!/usr/bin/env bash
pidfile=/var/run/face_publisher.pid
if [ -e $pidfile ]; then
pid=`cat $pidfile`
if kill -0 &>1 > /dev/null $pid; then
echo "Already running"
exit 1
else
rm $pidfile
fi
fi
echo $$ > $pidfile
cd /home/pi/laptracker/lap-tracker-client
sudo -b python face_publisher.py -l $1
cd /
rm $pidfile
