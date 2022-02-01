import re
from pprint import pprint

from django.conf import settings
from django.conf.urls.static import serve
from django.contrib import admin
from django.urls import path, include, re_path

urlpatterns = [
                  path('admin/', admin.site.urls),
                  path('', include('player.urls')),
                  path("__reload__/", include("django_browser_reload.urls")),
              ]
              # + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# this enables mediafiles to be served with DEBUG = False
urlpatterns.extend(
    [re_path(r'^%s(?P<path>.*)$' % re.escape(settings.MEDIA_URL.lstrip('/')), serve, kwargs={'document_root': settings.MEDIA_ROOT})]
)

pprint(urlpatterns)
