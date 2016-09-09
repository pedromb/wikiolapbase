from django.db import models
from mongoengine import *
import datetime

class Tags(EmbeddedDocument):
    column = StringField()
    colTags = ListField() 

class Levels(EmbeddedDocument):
    level = IntField()
    column = StringField()

class Hierarchies(EmbeddedDocument):
    hierarchy = StringField()
    levels = ListField(EmbeddedDocumentField(Levels))

class Metadata(Document):
    tableId = StringField()
    title = StringField()
    description = StringField()
    source = StringField()
    columns = ListField()
    tags = ListField(EmbeddedDocumentField(Tags))
    hierarchies = ListField(EmbeddedDocumentField(Hierarchies))
    created_at = DateTimeField(default=datetime.datetime.now)
    updated_at = DateTimeField(default=datetime.datetime.now)
    meta = {
        'indexes': [
            {
                'fields': ['$title', '$description', '$columns', '$tags.colTags'],
                'default_language': 'portuguese',
                'weights': {'title':10, 'description':8, 'columns':6, 'colTags': 5}
            }
        ]
    }