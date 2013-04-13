# -*- coding: utf-8 -*-

from django.views.generic import ListView

from braces.views import SetHeadlineMixin
from braces.views import LoginRequiredMixin

from tags.views import TagSearchMixin
from articles.models import Article


class FrontpageView(TagSearchMixin, LoginRequiredMixin, SetHeadlineMixin, ListView):
    login_url = "/"
    headline = 'Nyheter'
    queryset = Article.objects.filter(
        mod_tags__name__iexact="FRONTPAGE")
    context_object_name = 'article_list'
    paginate_by = 10
    template_name = 'frontpage.html'
