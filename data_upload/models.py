from django.db import models
from mongoengine import *
import datetime
# Create your models here.

class Tags(EmbeddedDocument):
    column = StringField()
    colTags = ListField() 

class Hierarchies(EmbeddedDocument):
    hierarchy = StringField()
    level = IntField()
    column = StringField()

class Metadata(Document):
    title = StringField()
    description = StringField()
    source = StringField()
    columns = ListField()
    tags = ListField(EmbeddedDocumentField(Tags))
    hierarchies = ListField(EmbeddedDocumentField(Hierarchies))
    created_at = DateTimeField(default=datetime.datetime.now)
    updated_at = DateTimeField(default=datetime.datetime.now)