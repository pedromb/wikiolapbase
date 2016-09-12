from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from rest_api import views

urlpatterns = [
    url(r'^api/searchmetadata/(?P<keywords>[\w,]+)/$', views.SearchMetadata.as_view()),
    url(r'^api/getdata/(?P<tableId>[\w,]+)/(?P<limit>[0-9]+)/$', views.GetData.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)