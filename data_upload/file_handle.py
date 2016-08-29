import pandas as pd
from data_upload.cassandra_handle import *
from django.core.cache import cache
import uuid

def handle_uploaded_file(session, file):
    df = pd.read_csv(file,encoding = "latin1")
    session_id = uuid.uuid4().urn[9:]
    session['session_id'] = session_id
    cache_id = 'my_data_set_' + session_id
    print(cache_id)
    cache.set(cache_id, df)