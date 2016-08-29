from mongoengine import connect
from data_upload.models import Metadata

def saveMetadata(form):
    metadata = Metadata(title=form['title'][0], source=form['source'][0], description = form['description'][0])
    metadata.save()
    return metadata