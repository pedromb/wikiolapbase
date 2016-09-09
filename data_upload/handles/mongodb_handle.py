from mongoengine import connect
from data_upload.models import Metadata
import json

def saveMetadata(metadata):
    metadata.save()

def getMetadata(jsonRequest):
    metadata = Metadata.from_json(jsonRequest)
    return metadata