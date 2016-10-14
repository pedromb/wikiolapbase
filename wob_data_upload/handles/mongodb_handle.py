from wob_data_upload.models import Metadata
from mongoengine import connect
import json

def saveMetadata(metadata):
    metadata.save()

def getMetadata(jsonRequest):
    metadata = Metadata.from_json(jsonRequest)
    return metadata