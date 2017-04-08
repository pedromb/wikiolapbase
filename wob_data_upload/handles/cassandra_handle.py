from wob_data_upload.handles.spark_handle import SparkCassandra
from cassandra.cluster import Cluster
from django.core.cache import cache
from unicodedata import normalize
from datetime import timedelta
import pandas as pd
import numpy as np
import time
import os

def getDevConnection():
    cluster = Cluster([os.environ['CASSANDRA_PORT_9042_TCP_ADDR']])
    metadata = cluster.metadata
    session = cluster.connect('cassandra_dev')
    print("Conectado ao cluster cassandra: " +metadata.cluster_name)
    return session

def closeConnection(session):
    session.cluster.shutdown()
    session.shutdown()
    print("Conexao ao cluster cassandra {} fechada".format(session.cluster.metadata.cluster_name))

def createTableFromDataFrame(table_name, alias_column_names, real_column_names, df):
    session = getDevConnection()
    query = 'CREATE TABLE '+table_name+' ( id bigint, '
    for (f,s) in zip(alias_column_names,real_column_names):
        col = f
        f = normalize('NFKD', f).encode('ascii', 'ignore').decode('ascii')
        f = f.lower().strip().replace(' ','_')
        query += f+" "+getCassandraTypeFromDf(df,s)+", "
    query += " PRIMARY KEY(id));"
    session.execute(query)
    print("Tabela "+table_name+" criada")
    closeConnection(session)

def dropTableFromCassandra(table_name):
    session = getDevConnection()
    query = 'DROP TABLE '+table_name+';'
    session.execute(query)
    print("Tabela "+table_name+" deletada")
    closeConnection(session)

def insertIntoTableFromDataFrame(table_name, df, alias_column_names):
    df['id'] = range(len(df.index))
    df = np.round(df, decimals=1)
    alias_column_names.append('id')
    my_tuples = [tuple(x) for x in df.values]
    rdd = SparkCassandra.sc.parallelize([{ 
            alias_column_names[index].lower().strip().replace(' ','_'):value 
            if not isinstance(value, np.float64) else float(value) \
            for index,value in enumerate(tuple_entry)
        } for tuple_entry in my_tuples
        ])

    rdd.saveToCassandra( \
        "cassandra_dev", \
        table_name
    )


def processDfToCassandra(session, metadata):
    session_id = session['session_id']
    cache_id = 'my_data_set_' + session_id
    df = cache.get(cache_id)
    alias_column_names = metadata.aliasColumns
    real_column_names = metadata.originalColumns
    table_name = metadata.tableId
    try:
        createTableFromDataFrame(table_name, alias_column_names, real_column_names,df)
    except:
        raise Exception("Error when creating table on Cassandra")
    try:
        insertIntoTableFromDataFrame(table_name, df, alias_column_names)
    except:
        dropTableFromCassandra(table_name)
        raise Exception("Error when adding data to table on Cassandra")

def getCassandraTypeFromDf(df, col):
    switcher = {
        'float64':'double',
        'int64':'bigint',
        'object':'text'
    }
    return(switcher.get(str(df[col].dtypes), 'text'))