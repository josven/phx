from django.conf.urls import patterns, url
from django.conf import urls

urlpatterns = patterns('',
    url(r'^old$', 'forum.views.read_old_forum', name='read_forum'),
    
    url(r'^thread/create/$', 'forum.views.create_thread', name='create_thread'),
    url(r'^thread/create/(?P<tags>(.+)(,\s*.+)*)/', 'forum.views.create_thread', name='create_thread_by_tags'),

    url(r'^thread/read/(?P<id>\d*)/$', 'forum.views.read_thread', name='read_thread'),
    
    url(r'^tags/(?P<tags>(.+)(,\s*.+)*)/$', 'forum.views.get_threads_by_tags', name='get_threads_by_tags'),


    url(r'^forumpost/create/$', 'forum.views.create_forumpost', name='create_forumpost'),
    
    url(r'^forumpost/reply/$', 'forum.views.create_forumpost', name='reply_on_forumpost'),
    url(r'^forumthread/reply/$', 'forum.views.create_forumpost', name='reply_on_thread'),
    
    
    #json for datatables
    url(r'^list/json/$', 'forum.views.list_forum_json', name='list_forum_json'),
    url(r'^tag/(?P<tags>(.+)(,\s*.+)*)/json/$', 'forum.views.list_forum_json', name='list_forum_json'),    
    
    
    
    url(r'^list/$', 'forum.views.list_forum', name='list_forum'),
    url(r'^tag/(?P<tags>(.+)(,\s*.+)*)/$', 'forum.views.list_forum', name='list_forum'),
    
    url(r'^read/(?P<id>\d*)/$', 'forum.views.read_forum', name='read_forum'),
    
    url(r'^create/(?P<tags>(.+)(,\s*.+)*)/$', 'forum.views.create_forum', name='create_forum'),
    url(r'^create/$', 'forum.views.create_forum', name='create_forum'),
    
        
    url(r'^read/(?P<forum_id>\d*)/comment/$', 'forum.views.comment_forum', name='comment_forum'),
    url(r'^read/(?P<id>\d*)/comment/(?P<comment_id>\d*)/$', 'forum.views.read_forum', name='read_forum_comment'),


    
)
