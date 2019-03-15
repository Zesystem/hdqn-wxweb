#!/bin/bash
NAME="app_wechat"
FLASKDIR=/root/hdqn-wxweb
UWSGIPATH=/root/.pyenv/shims/uwsgi
UWSGICONF=/root/hdqn-wxweb/uwsgi.ini
PYENVPATH=/root/.pyenv/bin/pyenv

echo "starting $NAME as `whoami`"
cd $FLASKDIR
exec $PYENVPATH local env367
export FLASK_CONFIG=production && exec $UWSGIPATH $UWSGICONF
echo "success to start $NAME application"
