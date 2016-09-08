from pyspark import SparkContext, SparkConf
from pyspark_cassandra import CassandraSparkContext

class SparkCassandra:
    appName = "WikiOlap"
    master = "spark://pedro-linux:7077"
    conf = SparkConf() \
        .setAppName(appName) \
        .setMaster(master) \
        .set("spark.cassandra.connection.host", "localhost")
    sc = CassandraSparkContext(conf=conf)