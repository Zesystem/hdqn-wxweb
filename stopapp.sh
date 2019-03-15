#!/bin/bash
NAME="app_wechat"
FLASKDIR=/root/hdqn-wxweb
UWSGIPATH=/root/.pyenv/shims/uwsgi
UWSGICONF=/root/hdqn-wxweb/uwsgi.ini

echo "stopping $NAME as `whoami`"
killall -9 uwsgi
echo "success to stop $NAME application" 
