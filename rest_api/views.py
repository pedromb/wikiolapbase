from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from mongoengine import QuerySet
from data_upload.models import Metadata
from data_upload.handles.spark_handle import SparkCassandra
from pyspark_cassandra import RowFormat
from pyspark.sql.functions import *
import pandas as pd
import json

class SearchMetadata(APIView):
    """
    Search for metadata based on keywords

    params:
        -keywords: list of keywords to query the metadata repository
            -type: string separated by commas

    endpoint: /searchmetadata/{keywords}

    Example: /searchmetadata/divida,estado,municipio

    """
    def get(self, request, keywords, format=None):
        try:
            mongoKeywords = keywords.replace(',', ' ')
            objects = Metadata.objects.search_text(mongoKeywords).order_by('$text_score')
            data = json.loads(objects.to_json())
            if (not data):
                content = {'Message':"No data matching your search was found"}
                return Response(content,status=status.HTTP_404_NOT_FOUND)
            else:
                return Response(data, status=status.HTTP_200_OK)
        except:
            content = {'Message':"Any error ocurred"}
            return Response(content, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class GetData(APIView):
    """
    Retrieve data from repository
    """

    def get(self, request, tableId, limit=None, selectColumns=None, groupBy=None, aggFunc=None, aggColumns=None, format=None):
        try:
            if not limit is None:
                jsonResponse = SparkCassandra.sc \
                    .cassandraTable("cassandra_dev", tableId, row_format = RowFormat.DICT) \
                    .limit(int(limit)) \
                    .collect()
            else:
                jsonResponse = SparkCassandra.sc \
                    .cassandraTable("cassandra_dev", tableId,row_format=RowFormat.DICT) \
                    .collect()

            if not groupBy is None:
                data = aggregateDataFromDict(groupBy,aggColumns,aggFunc,jsonResponse)
                jsonResponse = [json.loads(s) for s in data.toJSON().collect()]

            elif not selectColumns is None:
                data = selectColumnsFromDict(jsonResponse, selectColumns)
                jsonResponse = [json.loads(s) for s in data.toJSON().collect()]
    

            return Response(jsonResponse, status=status.HTTP_200_OK)

        except:
            content = {'Message':"Any error ocurred"}
            return Response(content, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class JoinData(APIView):
    """
    Retrieve data from repository

    """

    def get(self, request, tableIdRoot, tableIdJoin, columnsRoot, columnsJoin, 
        selectColumns=None, groupBy=None, aggFunc=None, aggColumns=None, limit=None, format=None):
        # try:
            ##Get data from one table
            dataRoot  = SparkCassandra.sc \
                .cassandraTable("cassandra_dev", tableIdRoot,  row_format = RowFormat.DICT) \
                .collect()
            dataRoot = SparkCassandra.sc.parallelize(dataRoot)

            ##Get data from other table
            dataToJoin = SparkCassandra.sc \
                .cassandraTable("cassandra_dev", tableIdJoin,  row_format = RowFormat.DICT) \
                .collect()
            dataToJoin = SparkCassandra.sc.parallelize(dataToJoin)

            ##Transform data to Spark DataFrame
            dfRoot = SparkCassandra.sqlContext.createDataFrame(dataRoot)
            dfToJoin = SparkCassandra.sqlContext.createDataFrame(dataToJoin)

            ##Rename columns to make them unique
            joinOnRoot = commaSeparatedToArray(columnsRoot)
            joinOnToJoin = commaSeparatedToArray(columnsJoin)
            columnsRoot = ["{}_{}".format(tableIdRoot, x) for x in joinOnRoot ]
            columnsJoin = ["{}_{}".format(tableIdJoin, x) for x in joinOnToJoin ]

            oldColumnsRoot = dfRoot.schema.names
            oldColumnsToJoin = dfToJoin.schema.names
            newColumnsRoot = [ "{}_{}".format(tableIdRoot, x) for x in oldColumnsRoot  ]
            newColumnsToJoin = [ "{}_{}".format(tableIdJoin, x) for x in oldColumnsToJoin ]
            dfRoot = dfRoot.toDF(*newColumnsRoot)
            dfToJoin  = dfToJoin.toDF(*newColumnsToJoin)

            ##Join tables on selected columnns
            joinedData = dfRoot.alias(tableIdRoot).join(\
                dfToJoin.alias(tableIdJoin), \
                [dfRoot[f] == dfToJoin[s] \
                for (f, s) in zip(columnsRoot, columnsJoin)], \
                'inner')
                
            ##Drop duplicate columns
            index = 0
            for (f,s) in zip(columnsRoot, columnsJoin):
                joinedData = joinedData.drop(s).withColumnRenamed(f,joinOnRoot[index])
                index=index+1

            if not groupBy is None:
                joinedData = aggregateDataFromDf(groupBy,aggColumns,aggFunc,joinedData)

            if not selectColumns is None:
                selectColumnsFiltered = [ "{}_{}".format(tableIdJoin, x) \
                if x not in joinOnToJoin else x \
                for x in oldColumnsToJoin ]
                selectedColumns = commaSeparatedToArray(selectColumns)
                joinedData = dataDf.select(*selectedColumns)

            if not limit is None:
                joinedData = joinedData.limit(int(limit))

            jsonResponse = [json.loads(s) for s in joinedData.toJSON().collect()]

            return Response(jsonResponse, status=status.HTTP_200_OK)
        # except:
            content = {'Message':"Any error ocurred"}
            return Response(content, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

def aggregateData(groupBy, aggFunc, aggColumn, data):
    dispatcher = {
        'sum':data.groupBy(*groupBy).sum,
        'avg':data.groupBy(*groupBy).avg
    }
    return dispatcher[aggFunc](*aggColumn)

def aggregateDataFromDf(groupBy, aggColumns, aggFunc, myDf):
    columnsToGroupBy = commaSeparatedToArray(groupBy)
    columnsToAggregate = commaSeparatedToArray(aggColumns)
    groupedData = aggregateData(columnsToGroupBy, aggFunc, columnsToAggregate, myDf)
    return groupedData

def aggregateDataFromDict(groupBy, aggColumns, aggFunc, myDict):
    columnsToGroupBy = commaSeparatedToArray(groupBy)
    columnsToAggregate = commaSeparatedToArray(aggColumns)
    myData = SparkCassandra.sc.parallelize(myDict)
    dataDf = SparkCassandra.sqlContext.createDataFrame(myData)
    groupedData = aggregateData(columnsToGroupBy, aggFunc, columnsToAggregate, dataDf)
    return groupedData

def selectColumnsFromDf(myDf, selectColumns):
    selectedColumns = commaSeparatedToArray(selectColumns)
    selectedData = myDf.select(*selectedColumns)
    return selectedData

def selectColumnsFromDict(myDict, selectColumns):
    selectedColumns = commaSeparatedToArray(selectColumns)
    myData = SparkCassandra.sc.parallelize(myDict)
    dataDf = SparkCassandra.sqlContext.createDataFrame(myData)
    selectedData = dataDf.select(*selectedColumns)
    return selectedData

def commaSeparatedToArray(commaSeparatedString):
    return list(filter(None,commaSeparatedString.split(',')))