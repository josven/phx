# -*- coding: utf-8 -*-

import re
from django.db import models
from django.core.exceptions import ValidationError


class UserTags(models.Model):
    name = models.CharField(max_length=255)
    main_article_category = models.BooleanField(default=False)

    def __unicode__(self):
        return self.name

    def clean(self, *args, **kwargs):
        # Test if tag is valid formated
        test = re.compile('^[0-9a-zA-Z ]+$')
        if test.match(self.name) is None:
            raise ValidationError('Taggen är inte giltig')
            
        super(UserTags, self).clean(*args, **kwargs)


class ModTags(models.Model):
    name = models.CharField(max_length=255)

    def __unicode__(self):
        return self.name

    def clean(self, *args, **kwargs):

        # Test if tag is valid formated
        test = re.compile('^[0-9a-zA-Z ]+$')
        test.match(self.name)
        if test is None:
            raise ValidationError('Taggen är inte giltig')
            
        super(ModTags, self).clean(*args, **kwargs)