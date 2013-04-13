# -*- coding: utf-8 -*-

from django.db import models
from django.db.models import get_model

from core.models import Entry, EntryHistory

from phx import site_strings

class Post(Entry):
    """
    A Post in the chat.

    """
    text = models.CharField(max_length=1024, help_text=site_strings.COMMENT_FORM_HELP_TEXT)