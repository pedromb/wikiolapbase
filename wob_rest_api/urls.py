from wob_rest_api import views
from rest_framework.urlpatterns import format_suffix_patterns
from django.conf.urls import url

urlpatterns = [
    url(r'^api/searchmetadata/(?P<keywords>[\w,]+)/$', views.SearchMetadata.as_view()),
    url(r'^api/getdata/(?P<tableId>\w+)/$', views.GetData.as_view()),
    url(r'^api/getdata/(?P<tableId>\w+)/(?P<limit>[0-9]+)/$', views.GetData.as_view()),
    url(r'^api/getdata/(?P<tableId>\w+)/(?P<selectColumns>[\w,]+)/$', views.GetData.as_view()),
    url(r'^api/getdata/(?P<tableId>\w+)/(?P<selectColumns>[\w,]+)/(?P<limit>[0-9]+)/$', views.GetData.as_view()),
    url(r'^api/getdata/(?P<tableId>\w+)/(?P<groupBy>[\w,]+)/(?P<aggFunc>\w+)/(?P<aggColumns>[\w,]+)/$', views.GetData.as_view()),
    url(r'^api/getdata/(?P<tableId>\w+)/(?P<groupBy>[\w,]+)/(?P<aggFunc>\w+)/(?P<aggColumns>[\w,]+)/(?P<limit>[0-9]+)/$', views.GetData.as_view()),
    url(r'^api/joindata/(?P<tableIdRoot>\w+)/(?P<tableIdJoin>\w+)/(?P<columnsRoot>[\w,]+)/(?P<columnsJoin>[\w,]+)/$', views.JoinData.as_view()),
    url(r'^api/joindata/(?P<tableIdRoot>\w+)/(?P<tableIdJoin>\w+)/(?P<columnsRoot>[\w,]+)/(?P<columnsJoin>[\w,]+)/(?P<limit>[0-9]+)/$', views.JoinData.as_view()),
    url(r'^api/joindata/(?P<tableIdRoot>\w+)/(?P<tableIdJoin>\w+)/(?P<columnsRoot>[\w,]+)/(?P<columnsJoin>[\w,]+)/(?P<groupBy>[\w,]+)/(?P<aggFunc>[\w,]+)/(?P<aggColumns>[\w,]+)/$', views.JoinData.as_view()),
    url(r'^api/joindata/(?P<tableIdRoot>\w+)/(?P<tableIdJoin>\w+)/(?P<columnsRoot>[\w,]+)/(?P<columnsJoin>[\w,]+)/(?P<groupBy>[\w,]+)/(?P<aggFunc>[\w,]+)/(?P<aggColumns>[\w,]+)/(?P<limit>[0-9]+)/$', views.JoinData.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)