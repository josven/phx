from django.conf.urls import patterns, url
from django.conf import urls

from .views import FrontpageView

urlpatterns = patterns(
    '',
    url(
        regex=r'^framsidan/$',
        view=FrontpageView.as_view(),
        name='start'
    ),
    url(
        regex=r'^framsidan/$',
        view=FrontpageView.as_view(),
        name='read_frontpage'
    )
)
