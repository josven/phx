from django.conf.urls import patterns, url
from django.conf import urls

urlpatterns = patterns('',
    #All settings
    url(r'^settings$', 'settings.views.read_settings', name='read_settings'),
    url(r'^(?P<appname>\w*)/settings$', 'settings.views.read_settings', name='read_settings'),
)
