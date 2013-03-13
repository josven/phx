from django.conf.urls import url
from django.conf.urls import patterns

from .views import LoginView
from .views import RegisterView
from .views import AboutView

urlpatterns = patterns(
    '',
    url(
        regex=r'^$',
        view=LoginView.as_view(),
        name='startpage'
    ),
    url(
        regex=r'^$',
        view=LoginView.as_view(),
        name='login_view'
    ),
    url(
        regex=r'^auth/logout/$',
        view='django.contrib.auth.views.logout',
        kwargs={'next_page': '/'},
        name='logout'
    ),
    url(
        regex=r'^auth/register/$',
        view=RegisterView.as_view(),
        name='register_view'
    ),
    url(
        regex=r'^about/$',
        view=AboutView.as_view(),
        name='about_view'
    ),
    url(
        regex=r'^auth/reset-password/$',
        view='django.contrib.auth.views.password_reset',
        kwargs={'email_template_name': 'email_reset_password_template.html',
                'template_name': 'reset_password.html',
                'post_reset_redirect': '/auth/reset-password-done/'},
        name='reset_password'
    ),
    url(
        regex=r'^auth/reset-password-confirm/(?P<uidb36>[0-9A-Za-z]+)/'
        '(?P<token>.+)/$',
        view='django.contrib.auth.views.password_reset_confirm',
        kwargs={'post_reset_redirect': '/auth/reset-password-complete/',
                'template_name': 'password_reset_confirm.html',
                'extra_context': {'app_name': 'registration'}},
        name='reset_password_confirm'
    ),
    url(
        regex=r'^auth/reset-password-done/$',
        view='django.contrib.auth.views.password_reset_done',
        kwargs={'template_name': 'reset_password_done.html'},
        name='reset_password_done'
    ),
    url(
        regex=r'^auth/reset-password-complete/$',
        view='django.contrib.auth.views.password_reset_complete',
        kwargs={'template_name': 'reset_password_complete.html'},
        name='reset_password_complete'
    ),
)
