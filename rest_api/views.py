from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from mongoengine import QuerySet
from data_upload.models import Metadata
from data_upload.handles.spark_handle import SparkCassandra
from pyspark_cassandra import RowFormat
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

    params:
        -tableId: tableId from table can be retrieved from metadata.
            type: string
        -limit: number of rows to retrieve. send 0 to retrieve all
            -type: integer - only accepts numbers bigger than zero

    endpoint: /getdata/{tableId}/{limit}/

    """

    def get(self, request, tableId, limit, format=None):
        try:
            if(int(limit) != 0):
                data = SparkCassandra.sc \
                    .cassandraTable("cassandra_dev", tableId, row_format=RowFormat.DICT) \
                    .limit(int(limit)) \
                    .collect()
            else:
                data = SparkCassandra.sc \
                    .cassandraTable("cassandra_dev", tableId,row_format=RowFormat.DICT) \
                    .collect()
            return Response(data, status=status.HTTP_200_OK)
        except:
            content = {'Message':"Any error ocurred"}
            return Response(content, status=status.HTTP_500_INTERNAL_SERVER_ERROR)