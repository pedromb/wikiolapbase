from django.conf.urls import include, url
from . import views

urlpatterns = [
    url(r'^$', views.wiki_olap_home),
    url(r'^wiki_olap_help/$', views.wiki_olap_help),
    url(r'^upload_file/$', views.upload_file),
    url(r'^upload_metadata/$', views.upload_metadata),
    url(r'^upload_file_action/$', views.upload_file_action),
    url(r'^upload_metadata_action/$', views.upload_metadata_action),
]