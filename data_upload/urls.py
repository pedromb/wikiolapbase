from django.conf.urls import include, url
from . import views

urlpatterns = [
    url(r'^$', views.upload_file_form),
    url(r'^upload_file_action/$', views.upload_file_action),
    url(r'^upload_metadata_form/$', views.upload_metadata_form),
    url(r'^upload_metadata_action/$', views.upload_metadata_action),
]