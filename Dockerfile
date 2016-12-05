##This is for local development only!

FROM ubuntu:xenial
MAINTAINER Pedro Magalhães Bernardo  <pedromagalhaesbernardo@gmail.com>

#OS dependences
RUN apt-get update && apt-get install -y \
    git \
    python3.5 \ 
    python3.5-dev \
    python3-pip \
    python3-setuptools \ 
    make \
    python2.7 \
    python-pip \
    tar \
    wget \
    curl

##Python dependences
RUN pip3 install django djangorestframework pandas pymongo mongoengine cassandra-driver django-cassandra-engine

##Install Java
RUN apt-get install -y openjdk-8-jdk

##Install Scala
ENV SCALA_VERSION 2.10.6
ENV SBT_VERSION 0.13.12

## Piping curl directly in tar
RUN curl -fsL http://downloads.typesafe.com/scala/$SCALA_VERSION/scala-$SCALA_VERSION.tgz | tar xfz - -C /root/ && \
  echo >> /root/.bashrc && \
  echo 'export PATH=~/scala-$SCALA_VERSION/bin:$PATH' >> /root/.bashrc

# Install sbt
RUN \
  curl -L -o sbt-$SBT_VERSION.deb http://dl.bintray.com/sbt/debian/sbt-$SBT_VERSION.deb && \
  dpkg -i sbt-$SBT_VERSION.deb && \
  rm sbt-$SBT_VERSION.deb && \
  apt-get update && \
  apt-get install sbt && \
  sbt sbtVersion

##Download Spark 1.6
RUN wget http://d3kbcqa49mib13.cloudfront.net/spark-1.6.2-bin-hadoop2.6.tgz
RUN tar -zxvf spark-1.6.2-bin-hadoop2.6.tgz -C /opt/
RUN rm spark-1.6.2-bin-hadoop2.6.tgz

##Add config to Spark
RUN echo "spark.jars.packages TargetHolding:pyspark-cassandra:0.3.5" >> /opt/spark-1.6.2-bin-hadoop2.6/conf/spark-defaults.conf.template
RUN mv /opt/spark-1.6.2-bin-hadoop2.6/conf/spark-defaults.conf.template /opt/spark-1.6.2-bin-hadoop2.6/conf/spark-defaults.conf

##Clone pyspark-cassanda
RUN git clone https://github.com/TargetHolding/pyspark-cassandra.git  /opt/pyspark-cassandra

##Environment variables
ENV JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64
ENV SPARK_HOME=/opt/spark-1.6.2-bin-hadoop2.6
ENV PATH=$PATH:/opt/spark-1.6.2-bin-hadoop2.6/bin/
ENV PYSPARK_PYTHON=/usr/bin/python3
ENV PYTHONPATH=$SPARK_HOME/python/:$PYTHONPATH
ENV PYTHONPATH=$SPARK_HOME/python/lib/py4j-0.9-src.zip:$PYTHONPATH
ENV PYTHONPATH=/opt/pyspark-cassandra/python/:$PYTHONPATH

RUN git clone https://github.com/pedromb/wikiolapbase

EXPOSE 8000

ADD entrypoint.sh /entrypoint.sh
CMD /entrypoint.sh