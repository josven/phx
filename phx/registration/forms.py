# -*- coding: utf-8 -*-

from django.contrib.auth.forms import UserCreationForm as DC
from django.contrib.auth.forms import AuthenticationForm as DA
from django import forms
from django.contrib.auth.models import User


class UserCreationForm(DC):
    email = forms.EmailField(label="Email")


class AuthenticationForm(DA):
    keep_session = forms.BooleanField(
        required=False,
        label='Håll mig inloggad'
    )
