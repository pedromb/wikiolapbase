from wikiolap_data_upload.handles.mongodb_handle import *
from wikiolap_data_upload.handles.spark_handle import *
from wikiolap_data_upload.handles.file_handle import *
from wikiolap_data_upload.models import *
from wikiolap_data_upload.forms import *
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.shortcuts import render
from django.core.cache import cache
import pandas as pd
import json

def wiki_olap_home(request):
    return render(request, 'wiki_olap_home.html')

def wiki_olap_help(request):
    return render(request, 'wiki_olap_help.html')

def upload_file(request):
    return render(request, 'upload_file.html')

def search_metadata(request):
    return render(request, 'search_metadata.html')

def upload_metadata(request):
    session_id = request.session['session_id']
    data_cache_id = 'my_data_set_' + session_id
    df = cache.get(data_cache_id)
    if df is None:
         return render(request, 'upload_file.html')
    columnNames = list(df.columns.values)
    previewDf = df.head(10)
    previewDict = previewDf.to_dict()
    data = []
    for index, row in previewDf.iterrows():
        newEntry = []
        for column in columnNames:
            newEntry.append(row[column])
        data.append(newEntry)
    return render(request, 'upload_metadata.html', {"columnNames":columnNames, "data": data})

@csrf_exempt
def upload_file_action(request):
    if request.method == 'POST':    
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            session = request.session
            handle_uploaded_file(session, request.FILES['file'])
            return HttpResponseRedirect('/upload_metadata')

@csrf_exempt
def upload_metadata_action(request): 
    jsonRequest = request.body.decode('utf-8')
    jsonDecoded = json.loads(jsonRequest)
    session_id = request.session['session_id']
    tableId = jsonDecoded['title'].strip().replace(' ','_')+'_'+session_id[:8].replace('-','_')
    jsonDecoded['tableId'] = normalize('NFKD', tableId).encode('ascii', 'ignore').decode('ascii').lower()
    metadataJson = json.dumps(jsonDecoded)
    metadata = getMetadata(metadataJson)
    test = cache.get(session_id)
    if test is None:
        return HttpResponse('Sessão expirada', status=440)
    try:
        saveMetadata(metadata)
    except:
        return HttpResponse('Ocorreu um erro ao salvar os metadados', status=500)
    try:
        processDfToCassandra(request.session, metadata)
    except:
        Metadata.objects(tableId=metadata.tableId).delete()
        return HttpResponse('Ocorreu um erro ao salvar os dados no repositório', status=500)
    data_cache_id = 'my_data_set_' + session_id
    cache.delete(data_cache_id)
    return HttpResponse('Ok',status=200)
