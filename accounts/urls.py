from django.conf.urls import patterns, url
from django.contrib.auth import views as auth_views


urlpatterns = patterns(
    '',
    url(
        regex=r'^passreset/$',
        view=auth_views.password_reset,
        name='forgot_password1'),
    url(
        regex=r'^passresetdone/$',
        view=auth_views.password_reset_done,
        name='forgot_password2'),
    url(
        regex=r'^passresetconfirm/(?P<uidb36>[-\w]+)/(?P<token>[-\w]+)/$',
        view=auth_views.password_reset_confirm,
        name='forgot_password3'),
    url(
        regex=r'^passresetcomplete/$',
        view=auth_views.password_reset_complete,
        name='forgot_password4'),
    url(
        regex=r'^password/change/$',
        view=auth_views.password_change,
        name='auth_password_change'),
    url(
        regex=r'^password/change/done/$',
        view=auth_views.password_change_done,
        name='auth_password_change_done'),
)
