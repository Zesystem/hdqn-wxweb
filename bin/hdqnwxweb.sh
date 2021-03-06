#!/bin/bash

cd /root/hdqn-wxweb

if [ ! -n "$1" ];then
    echo "Usages: sh hdqnwxweb.sh [start|stop|restart]"
    exit 0
fi

if [ $1 = start ];then
    service nginx start
    psid=`ps aux | grep "uwsgi" | grep -v "grep" | wc -l`        
    if [ $psid -gt 4 ];then
        echo "uwsgi is running!"
        exit 0 
    else
        /root/.pyenv/shims/uwsgi /root/hdqn-wxweb/conf/uwsgi.ini
        echo "Start uwsgi service [OK]"
    fi
elif [ $1 = stop ];then
    killall -9 uwsgi
    service nginx stop
    echo "Stop uwsgi service [OK]"
elif [ $1 = restart ];then
    service nginx restart
    killall -9 uwsgi
    /root/.pyenv/shims/uwsgi /root/hdqn-wxweb/conf/uwsgi.ini
    echo "Restart uwsgi service [OK]"
else
    echo "Usages: sh hdqnwxweb.sh [start|stop|restart]"
fi
