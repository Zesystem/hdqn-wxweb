#!/bin/bash

echo 'Starting to deploy hdqnwxweb service ...'
BASEPATH=$(cd `dirname $0`; pwd)
echo '==>Deploying from path: $BASHPATH ...'
echo '==>Create usergroup gid:1001 ...'
groupadd -g 1001 uwsgigroup
echo '==>Create user uid: 1001 ...'
useradd -u 1001 -g uwsgigroup uwsgi
echo '==>Copying file: $BASEPATH/conf/default.conf to: /etc/nginx/conf.d/default.conf ...'
cp $BASEPATH/conf/default.conf /etc/nginx/conf.d/default.conf
echo '==>Copying file: $BASEPATH/conf/hdqnwxwe to: /etc/init.d/hdqnwxweb ...'
cp $BASEPATH/conf/hdqnwxweb /etc/init.d/hdqnwxweb
echo 'Modifying the authority of deploy files ...'
chmod +x /etc/init.d/hdqnwxweb
chmod +x /etc/nginx/conf.d/default.conf
echo 'Add service to system ...'
chkconfig --add hdqnwxweb
chkconfig --level 345 hdqnwxweb on
chkconfig --list hdqnwxweb
echo 'Successfully deploy hdqnwxweb!'
echo 'Use `service hdqnwxweb start` to start service.'