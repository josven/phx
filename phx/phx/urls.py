from django.conf.urls import patterns
from django.conf.urls import include
from django.conf.urls import url
from django.conf import settings

from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^admin/', include(admin.site.urls)),
    (r'^', include('registration.urls')),
    #(r'^', include('frontpage.urls')),
    #(r'^', include('core.urls')),
    #(r'^', include('settings.urls')),
    #(r'^', include('guestbook.urls')),
    #(r'^forum/', include('forum.urls')),
    #(r'^user/', include('profiles.urls')),
    #(r'^chat/', include('chat.urls')),
    #(r'^notifications/', include('notifications.urls')),
    #(r'^', include('articles.urls')),
    #(r'^accounts/', include('accounts.urls')),

)

if settings.DEBUG:
    # static files (images, css, javascript, etc.)
    urlpatterns += patterns(
        '',
        url(
            regex=r'^(?P<path>.*)$',
            view='django.views.static.serve',
            kwargs={'document_root': settings.MEDIA_ROOT}
        )
    )
