from mongoengine import connect
from data_upload.models import Metadata
import json

def saveMetadata(jsonRequest):
    metadata = Metadata.from_json(jsonRequest)
    metadata.save()
    return metadata