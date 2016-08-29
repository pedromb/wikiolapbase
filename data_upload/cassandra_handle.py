from cassandra.cluster import Cluster
from cassandra.query import BatchStatement
from cassandra import ConsistencyLevel
from django.core.cache import cache
import pandas as pd
import uuid

def getDevConnection():
    cluster = Cluster()
    metadata = cluster.metadata
    session = cluster.connect('cassandra_dev')
    print("Conectado ao cluster: " +metadata.cluster_name)
    return session

def closeConnection(session):
    session.cluster.shutdown()
    session.shutdown()
    print("Conexão fechada")

def createTableFromDataFrame(table_name, column_names):
    session = getDevConnection()
    query = "CREATE TABLE "+table_name+" ( id uuid, "
    for i in column_names:
        query += i+" text, "
    query += " PRIMARY KEY(id));"
    session.execute(query)
    print("Tabela "+table_name+" criada")
    closeConnection(session)

def insertIntoTableFromDataFrame(table_name, column_names, dict_from_df, num_of_rows):
    query = "INSERT INTO "+table_name+" (id, "
    for idx, val in enumerate(column_names):
        if(idx != len(column_names)-1):
            query += val+", "
        else:
            query +=  val+") "
    query += "VALUES (?, "
    for i in range(0, len(column_names)):
        if(i != len(column_names)-1):
            query += "?, "
        else:
            query += "?);"
    session = getDevConnection()
    bound_statement = session.prepare(query)
    batch_statements = createBatchStatements(dict_from_df, column_names, num_of_rows, bound_statement)
    print(num_of_rows)
    print(len(batch_statements))
    for batch in batch_statements:
        session.execute(batch)
    closeConnection(session)

def createBatchStatements(dict_from_df, column_names, num_of_rows, bound_statement):
    arraysOfData = []
    arraysOfBatchs = []
    max_batch_size = 50
    for column in column_names:
        arraysOfData.append(list(dict_from_df[column].values()))
    batch_statement = BatchStatement(consistency_level=ConsistencyLevel.QUORUM)
    for i in range(num_of_rows):
        newEntry = []
        newEntry.append(uuid.uuid4())
        for array in arraysOfData:
            newEntry.append(str(array[i]))
        batch_statement.add(bound_statement, newEntry)
        if (i % max_batch_size == 0):
            arraysOfBatchs.append(batch_statement)
            batch_statement = BatchStatement(consistency_level=ConsistencyLevel.QUORUM)
    arraysOfBatchs.append(batch_statement)
    return arraysOfBatchs

def processDfToCassandra(session, metadata):
    session_id = session['session_id']
    cache_id = 'my_data_set_' + session_id
    print(cache_id)
    df = cache.get(cache_id)
    columnNames = list(df.columns.values)
    table_name = metadata.title.replace(' ', '_')
    print(table_name)
    df_dict = df.to_dict()
    df_size = df.shape[0]
    createTableFromDataFrame(table_name, columnNames)
    insertIntoTableFromDataFrame(table_name, columnNames, df_dict, df_size)