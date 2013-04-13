# -*- coding: utf-8 -*-
from django import forms
from django.forms import ModelForm

from models import Profile

from sorl.thumbnail import ImageField
from taggit.forms import TagField

from tags.models import UserTags

class SubscribeTagForm(ModelForm):

    class Meta:
        model = UserTags
        fields = ('name', )

# OLD STUFF BELOW
class ProfileForm(ModelForm):

    class Meta:
        model = Profile
        exclude = ('user','subscriptions','date_username_last_changed',)
        description = forms.CharField(help_text="Formateringshjälp: http://sv.wikipedia.org/wiki/Textile")

class ProfileDescriptionForm(ModelForm):

    class Meta:
        model = Profile
        fields = ('description',)
        description = forms.CharField(label="", help_text="", widget=forms.Textarea())


class ProfileSubscriptionsForm(ModelForm):
    subscriptions = TagField(label='Taggar')
    
    class Meta:
        model = Profile
        fields = ('subscriptions',)