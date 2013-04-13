from django.conf.urls import patterns, url
from django.conf import urls

from .views import ToggleUserTagFormView

urlpatterns = patterns('',
    url(
        regex=r'^(?P<user_id>\d*)/user_tags/$',
        view=ToggleUserTagFormView.as_view(),
        name='subscribe_tag'
    ),

    #url(r'^$', 'profiles.views.read_profile', name='read_profile'),
    #url(r'^(?P<user_id>\d*)/$', 'profiles.views.read_profile', name='read_profile'),
    #url(r'^update/$', 'profiles.views.update_profile', name='update_profile'),
    #Ajax APIs
    #url(r'^(?P<user_id>\d*)/description/form/$', 'profiles.views.profile_description_form', name='ajax_user_description_form'),

)
