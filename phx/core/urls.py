from django.conf.urls import patterns, url
from django.conf import urls
from views import PreviewView


urlpatterns = patterns('',
    url(
        regex=r'^utils/preview/$',
        view=PreviewView.as_view(),
        name='preview'
    ),

    #url(r'^utils/update-entry/(?P<app_label>\w*)/(?P<class_name>\w*)/(?P<id>\d*)/$', 'core.views.update_entry', name='update_entry'),
    #url(r'^utils/delete-entry/(?P<app_label>\w*)/(?P<class_name>\w*)/(?P<id>\d*)/$', 'core.views.delete_entry', name='delete_entry'),
    #url(r'^utils/history-entry/(?P<app_label>\w*)/(?P<class_name>\w*)/(?P<id>\d*)/$', 'core.views.history_entry', name='history_entry'),
    #url(r'^utils/subscribe-tag/$', 'core.views.subscribe_tag', name='subscribe_tag'),
)
