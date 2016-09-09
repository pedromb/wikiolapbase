from data_upload.handles.spark_handle import SparkCassandra
from cassandra.cluster import Cluster
from django.core.cache import cache
from datetime import timedelta
from unicodedata import normalize
import pandas as pd
import numpy as np
import time

def getDevConnection():
    cluster = Cluster()
    metadata = cluster.metadata
    session = cluster.connect('cassandra_dev')
    print("Conectado ao cluster cassandra: " +metadata.cluster_name)
    return session

def closeConnection(session):
    session.cluster.shutdown()
    session.shutdown()
    print("Conexão ao cluster cassandra {} fechada".format(session.cluster.metadata.cluster_name))

def createTableFromDataFrame(table_name, column_names):
    session = getDevConnection()
    query = 'CREATE TABLE '+table_name+' ( id text, '
    for i in column_names:
        i = normalize('NFKD', i).encode('ascii', 'ignore').decode('ascii')
        i = i.lower().strip().replace(' ','_')
        query += i+" text, "
    query += " PRIMARY KEY(id));"
    session.execute(query)
    print("Tabela "+table_name+" criada")
    closeConnection(session)

def insertIntoTableFromDataFrame(table_name, df):
    df['id'] = range(len(df.index))
    column_names = list(df.columns.values)
    my_tuples = [tuple(x) for x in df.values]
    rdd = SparkCassandra.sc.parallelize([{ \
        column_names[index].lower():str(value) for index,value in enumerate(tuple_entry) \
        } for tuple_entry in my_tuples])
    rdd.saveToCassandra( \
        "cassandra_dev", \
        table_name, \
        ttl = timedelta(hours=1) \
    )

def processDfToCassandra(session, metadata):
    session_id = session['session_id']
    cache_id = 'my_data_set_' + session_id
    df = cache.get(cache_id)
    column_names = list(df.columns.values)
    table_name = metadata.tableId
    createTableFromDataFrame(table_name, column_names)
    insertIntoTableFromDataFrame(table_name, df)