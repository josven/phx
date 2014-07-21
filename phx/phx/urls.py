from django.conf.urls import patterns
from django.conf.urls import include
from django.conf.urls import url
from django.conf import settings

from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^admin/', include(admin.site.urls)),
    (r'^accounts/', include('accounts.urls')),
)

