# -*- coding: utf-8 -*-

from datetime import timedelta

from django.core.urlresolvers import reverse_lazy
from django.contrib.auth import login
from django.contrib.auth.forms import PasswordResetForm
from django.views.generic import FormView
from django.views.generic import CreateView
from django.views.generic import TemplateView
from django.shortcuts import redirect

from braces.views import SetHeadlineMixin

from .forms import AuthenticationForm
from .forms import UserCreationForm

from profiles.models import Profile


class LoginView(SetHeadlineMixin, FormView):
    headline = "Välkommen till PHX!"
    template_name = 'login.html'
    form_class = AuthenticationForm
    success_url = reverse_lazy('start')

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            return redirect('start')
        return super(LoginView, self).dispatch(
            request, *args, **kwargs)

    def form_valid(self, form):
        user = form.get_user()
        login(self.request, user)   

        # If theres a user profile
        obj, created = Profile.objects.get_or_create(user=user)

        if self.request.POST.get('keep_session', None):
            self.request.session.set_expiry(timedelta(days=365))
        else:
            self.request.session.set_expiry(0)
        return super(LoginView, self).form_valid(form)


class RegisterView(SetHeadlineMixin, CreateView):
    headline = "Välkommen till PHX!"
    template_name = 'register.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('start')


class AboutView(SetHeadlineMixin, TemplateView):
    headline = "Välkommen till PHX!"
    template_name = 'about.html'


class ResetPasswordView(SetHeadlineMixin, FormView):
    headline = "xxx"
    template_name = 'reset_password.html'
    form_class = PasswordResetForm
    success_url = reverse_lazy('login_view')
