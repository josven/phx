from django.conf.urls import patterns, url
from django.conf import urls

from .views import ArticleListView
from .views import ArticleDetailView

urlpatterns = patterns('',  
    
    # Return all articles
    url(
        regex=r'^artiklar/$',
        view=ArticleListView.as_view(),
        name='list_articles'
    ),
    # Return a single article based on id
    url(
        regex=r'^artiklar/(?P<pk>\d*)/$',
        view=ArticleDetailView.as_view(),
        name='read_article'
    ),
    # Return a single article based on slug
    url(
        regex=r'^artiklar/(?P<slug>[-\w]+)/$',
        view=ArticleDetailView.as_view(),
        name='read_article'
    ),

    # OLD STUFF
    #json for datatables
    url(r'^articles/list/json/$', 'articles.views.list_articles_json', name='list_articles_json'),
    url(r'^articles/list/(?P<tags>(.+)(,\s*.+)*)/json/$', 'articles.views.list_articles_json', name='list_articles_json'),  
    url(r'^user/(?P<user_id>\d*)/(?P<tags>(.+)(,\s*.+)*)/json/$', 'articles.views.list_articles_json', name='list_articles_json'),
    url(r'^articles/tag/(?P<tags>(.+)(,\s*.+)*)/json/$', 'articles.views.list_articles_json', name='list_articles_json'),    


    
    # Create
    url(r'^articles/create/$', 'articles.views.create_article', name='create_article'),    
    url(r'^articles/tag/(?P<tags>(.+)(,\s*.+)*)/$', 'articles.views.search_article', name='search_article'),

    #Ajax APIs
    url(r'^articles/(?P<id>\d*)/body/form/$', 'articles.views.ajax_article_body_form', name='ajax_article_body_form'),
    url(r'^articles/(?P<article_id>\d*)/comments/$', 'articles.views.ajax_comments_article', name='ajax_comments_article'),

    #User url articles
    #url(r'^user/(?P<user_id>\d*)/articles/tag/(?P<tags>(.+)(,\s*.+)*)/$', 'articles.views.search_article', name='read_user_articles'),

    url(r'^user/(?P<user_id>\d*)/article/(?P<id>\d*)/$', 'articles.views.read_article', name='read_user_article'),  
    url(r'^user/(?P<user_id>\d*)/(?P<tags>(.+)(,\s*.+)*)/$', 'articles.views.search_article', name='read_user_articles'),
    
    # Comment articles
    url(r'^articles/(?P<article_id>\d*)/comment/$', 'articles.views.comment_article', name='comment_article'),
  

    
)
