from pyspark import SparkContext, SparkConf
from pyspark.sql import SQLContext
from pyspark_cassandra import CassandraSparkContext

class SparkCassandra:
    appNameCassandra = "WikiOlapCassandra"
    appNameSQL = "WikiOlapSQL"
    master = "spark://pedro-linux:7077"

    confCassandra = SparkConf() \
        .setAppName(appNameCassandra) \
        .setMaster(master) \
        .set("spark.cassandra.connection.host", "localhost")


    sc = CassandraSparkContext(conf=confCassandra)
    sqlContext = SQLContext(sc)