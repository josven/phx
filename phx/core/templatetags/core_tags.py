# -*- coding: utf-8 -*-

from django import template
from django.utils.http import urlencode

register = template.Library()

@register.simple_tag
def format_get_params(current_get_params, **kwargs):
    params = dict()

    # Format tags
    add_tag = kwargs.get('add_tag', None)
    remove_tag = kwargs.get('remove_tag', None)

    tags = current_get_params.get('tags', [])
    if tags:
        # Format tags into list
        tags = tags.split(',')
        tags = filter(None, tags)

    if add_tag:
        tags.append(add_tag)
    
    if remove_tag:
        tags = filter(lambda a: a != remove_tag, tags)

    # Format tags into string and push into new params
    if tags:
        params['tags'] = u','.join(tags)

    # Format rest of the params
    permitted_params = ['q', 'order', 'display']
    for keyword in permitted_params:

        current = current_get_params.get(keyword, None)
        if current:
            params[keyword] = current

        new = kwargs.get(keyword, None)
        if new:
            params[keyword] = new

    return urlencode(params)
