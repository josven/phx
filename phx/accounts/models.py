# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.humanize.templatetags.humanize import naturalday
from django.contrib.auth.models import User
from django.template.loader import render_to_string


class Users(User):

    @property
    def gender(self):
        return self.get_profile().gender

    @property
    def location(self):
        return self.get_profile().location

    @property
    def userlink(self):
        userlink_vars = render_userlink(self)
        return render_to_string('userlink_template.html', userlink_vars).replace('"','\"')

    @property
    def age(self):
        return calculate_age(self.get_profile().birthdate)

    @property
    def photo(self):
        profile = self.get_profile()
        if profile.photo:
            photo_url = get_thumbnail(profile.photo, '40x40', crop='center', quality=99).url
            photo = u'<img src=\"{0}\" />'.format(photo_url)
        else:
            photo = None
        return photo

    class Meta:
        proxy = True
        verbose_name = "Användare"
