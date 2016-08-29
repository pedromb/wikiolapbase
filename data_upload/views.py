import pandas as pd
from django.shortcuts import render
from data_upload.forms import *
from data_upload.file_handle import *
from data_upload.models import *
from django.views.decorators.csrf import csrf_exempt
from django.core.cache import cache
from django.http import HttpResponseRedirect
from data_upload.mongodb_handle import *

def upload_file_form(request):
    return render(request, 'upload_file_form.html',{})

def upload_metadata_form(request):
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
    return render(request, 'upload_metadata_form.html',{"columnNames":columnNames, "data": data})

@csrf_exempt
def upload_file_action(request):
    if request.method == 'POST':    
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            session = request.session
            handle_uploaded_file(session, request.FILES['file'])
            return HttpResponseRedirect('/upload_metadata_form')

@csrf_exempt
def upload_metadata_action(request):
    form = dict(request.POST)
    metadata = saveMetadata(form)
    processDfToCassandra(request.session, metadata)
    return HttpResponseRedirect('/')