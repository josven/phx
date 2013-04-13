# -*- coding: utf-8 -*-
import operator

from django.db.models import Q


class TagSearchMixin(object):

    def get_queryset(self):
        queryset = super(TagSearchMixin, self).get_queryset()
        tags = self.request.GET.get('tags', None)

        if tags:
            tags = tags.split(',')
            tags = filter(None, tags)

            if tags:
                query_list = []

                for tag in tags:
                    queryset = queryset.filter(user_tags__name=tag)

        return queryset
