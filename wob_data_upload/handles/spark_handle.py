from pyspark_cassandra import CassandraSparkContext
from pyspark import SparkContext, SparkConf
from pyspark.sql import SQLContext
import socket


class SparkCassandra:
    appNameCassandra = "WikiOlapCassandra"
    appNameSQL = "WikiOlapSQL"
    master = "spark://"+socket.gethostname()+":7077"

    confCassandra = SparkConf() \
        .setAppName(appNameCassandra) \
        .setMaster(master) \
        .set("spark.cassandra.connection.host", "localhost")


    sc = CassandraSparkContext(conf=confCassandra)
    sqlContext = SQLContext(sc)