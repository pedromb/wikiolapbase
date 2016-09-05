from django.db import models
from mongoengine import *
import datetime
# Create your models here.

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
    title = StringField()
    description = StringField()
    source = StringField()
    columns = ListField()
    tags = ListField(EmbeddedDocumentField(Tags))
    hierarchies = ListField(EmbeddedDocumentField(Hierarchies))
    created_at = DateTimeField(default=datetime.datetime.now)
    updated_at = DateTimeField(default=datetime.datetime.now)