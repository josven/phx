# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url
from django.conf import urls

urlpatterns = patterns('',    

     url(r'^$', 'notifications.views.notifications', name='read_notifications'),
     url(r'^delete/$', 'notifications.views.delete_notification', name='delete_notification'),
     url(r'^delete/$', 'notifications.views.delete_notification', name='delete_notifications'),
     url(r'^updates.(?P<format>\w*)$', 'notifications.views.updates', name='read_updates'),

)
