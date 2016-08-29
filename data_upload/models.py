from django.db import models
from mongoengine import *
import datetime
# Create your models here.

class Metadata(Document):
    title = StringField()
    description = StringField()
    #provenance = StringField()
    source = StringField()
    #columns = ListField()
    created_at = DateTimeField(default=datetime.datetime.now)
    updated_at = DateTimeField(default=datetime.datetime.now)