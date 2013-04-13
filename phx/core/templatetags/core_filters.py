import re

from django import template

register = template.Library()

@register.filter(is_safe=True)
def highlight(text, word):
    regexp = re.compile(re.escape(word), re.IGNORECASE)
    highlighted_word = u'<span class="text-success">{0}</span>'.format(word)
    return regexp.sub(highlighted_word, text)
