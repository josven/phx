from django.conf.urls import patterns, url
from django.conf import urls

urlpatterns = patterns('',

    # The chat
    url(r'^$', 'chat.views.chat', name='chat'),
    
    # Get chat, ajax api
    url(r'^get/$', 'chat.views.get_chat', name='get_chat'),
    
    # Post chat, ajax api
    url(r'^post/$', 'chat.views.post_chat', name='chat_post'),
    
    #Tinychat
     url(r'^camchat/$', 'chat.views.camchat', name='camchat'),
)
