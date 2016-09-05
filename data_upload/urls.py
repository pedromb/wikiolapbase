from django.conf.urls import include, url
from . import views

urlpatterns = [
    url(r'^$', views.upload_first_step),
    url(r'^upload_second_step/$', views.upload_second_step),
    url(r'^upload_third_step/$', views.upload_third_step),
    url(r'^upload_final_step/$', views.upload_final_step),
    url(r'^upload_file_action/$', views.upload_file_action),
    url(r'^upload_third_step_action/$', views.upload_third_step_action),
    url(r'^upload_final_step_action/$', views.upload_final_step_action),
    url(r'^upload_metadata_action/$', views.upload_metadata_action),
]