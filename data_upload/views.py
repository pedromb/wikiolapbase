import pandas as pd
from data_upload.forms import *
from data_upload.handles.file_handle import *
from data_upload.handles.mongodb_handle import *
from data_upload.models import *
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.core.cache import cache
from django.http import HttpResponseRedirect
from django.http import HttpResponse

import json

def upload_first_step(request):
    return render(request, 'upload_first_step.html')

def upload_second_step(request):
    return render(request, 'upload_second_step.html')

def upload_third_step(request):
    session_id = request.session['session_id']
    data_cache_id = 'my_data_set_' + session_id
    df = cache.get(data_cache_id)
    columnNames = list(df.columns.values)
    return render(request, 'upload_third_step.html',{"columnNames":columnNames})

def upload_final_step(request):
    session_id = request.session['session_id']
    cache_id = 'my_data_set_' + session_id
    df = cache.get(cache_id)
    columnNames = list(df.columns.values)
    previewDf = df.head(10)
    previewDict = previewDf.to_dict()
    data = []
    for index, row in previewDf.iterrows():
        newEntry = []
        for column in columnNames:
            newEntry.append(row[column])
        data.append(newEntry)
    return render(request, 'upload_final_step.html',{"columnNames":columnNames, "data": data})

@csrf_exempt
def upload_file_action(request):
    if request.method == 'POST':    
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            session = request.session
            handle_uploaded_file(session, request.FILES['file'])
            return HttpResponseRedirect('/upload_second_step')

@csrf_exempt
def upload_third_step_action(request):
    jsonRequest = request.body.decode('utf-8')
    session_id = request.session['session_id']
    metadata_cache_id = 'my_metadata' + session_id
    cache.set(metadata_cache_id,jsonRequest)
    return HttpResponse("OK")

@csrf_exempt
def upload_final_step_action(request):
    jsonRequest = request.body.decode('utf-8')
    session_id = request.session['session_id']
    print(jsonRequest)
    metadata_cache_id = 'my_metadata' + session_id
    oldJson = cache.get(metadata_cache_id)
    oldDict = json.loads(oldJson)
    requestDict = json.loads(jsonRequest)
    mergedDict = {**oldDict, **requestDict}
    jsonMerged = json.dumps(mergedDict)
    cache.set(metadata_cache_id,jsonMerged)
    return HttpResponse("OK")

@csrf_exempt
def upload_metadata_action(request):
    jsonRequest = request.body.decode('utf-8')
    session_id = request.session['session_id']
    data_cache_id = 'my_data_set_' + session_id
    metadata_cache_id = 'my_metadata' + session_id
    oldJson = cache.get(metadata_cache_id)
    oldDict = json.loads(oldJson)
    requestDict = json.loads(jsonRequest)
    mergedDict = {**oldDict, **requestDict}
    jsonMerged = json.dumps(mergedDict)
    metadata = saveMetadata(jsonMerged)
    processDfToCassandra(request.session, metadata)
    cache.delete(metadata_cache_id)
    cache.delete(data_cache_id)
    return HttpResponse("OK")