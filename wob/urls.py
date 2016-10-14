from django.conf.urls import include, url
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'', include('wob_data_upload.urls')),
    url(r'', include('wob_rest_api.urls'))
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
