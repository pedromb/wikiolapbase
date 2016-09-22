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
    originalColumns = ListField()
    aliasColumns = ListField()
    tags = ListField(EmbeddedDocumentField(Tags), default=list)
    hierarchies = ListField(EmbeddedDocumentField(Hierarchies),  default=list)
    email = StringField()
    created_at = DateTimeField(default=datetime.datetime.now)
    updated_at = DateTimeField(default=datetime.datetime.now)
    meta = {
        'indexes': [
            {
                'fields': ['$title', '$description', '$aliasColumns', '$originalColumns', '$tags.colTags'],
                'default_language': 'portuguese',
                'weights': {'title':10, 'description':8, 'aliasColumns':6, 'originalColumns':6, 'colTags': 5}
            }
        ]
    }