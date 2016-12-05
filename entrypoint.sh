#!/bin/bash
#Start spark master and slave
$SPARK_HOME/sbin/start-master.sh
$SPARK_HOME/sbin/start-slave.sh "spark://$HOSTNAME:7077"

##Sync cassandra to create keyspace
python3 wikiolapbase/manage.py sync_cassandra

##Start application
python3 wikiolapbase/manage.py runserver 0.0.0.0:8000