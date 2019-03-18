#!/bin/bash

echo 'Starting to deploy hdqnwxweb service ...'
BASEPATH=$(cd `dirname $0`; pwd)
echo '==>Deploying from path: $BASHPATH ...'
echo '==>Copying file: $BASEPATH/conf/default.conf to: /etc/nginx/conf.d/default.conf ...'
cp $BASEPATH/conf/default.conf /etc/nginx/conf.d/default.conf
echo '==>Copying file: $BASEPATH/conf/hdqnwxweb to: /etc/init.d/hdqnwxweb ...'
cp $BASEPATH/conf/hdqnwxweb /etc/init.d/hdqnwxweb
echo 'Installing dependency packages ...'
pip install -r $BASEPATH/requirements.txt
echo 'Modifying the authority of deploy files ...'
chmod +x /etc/init.d/hdqnwxweb
chmod +x /etc/nginx/conf.d/default.conf
echo 'Add service to system ...'
chkconfig --add hdqnwxweb
chkconfig --level 345 hdqnwxweb on
chkconfig --list hdqnwxweb
echo 'Timing restart service is being add ...'
crontab $BASEPATH/conf/rootcorn
crontab -l
echo 'Successfully deploy hdqnwxweb!'
echo 'Use `service hdqnwxweb start` to start service.'