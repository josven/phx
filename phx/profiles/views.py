# -*- coding: utf-8 -*-

from django.contrib.auth.models import User, Group
from django.http import Http404, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404, Http404
from django.views.decorators.cache import never_cache

from core.utils import render
from models import Profile
from .forms import ProfileForm
from .forms import ProfileDescriptionForm
from .forms import ProfileSubscriptionsForm


# NEW STUFF

from django.views.generic import FormView
from django.contrib import messages
from django.shortcuts import redirect

from .forms import SubscribeTagForm
from tags.models import UserTags


class ToggleUserTagFormView(FormView):
    template_name = 'forms/form_subscribe_tag.html'
    form_class = SubscribeTagForm
    success_url = '/thanks/'

    def form_valid(self, form):
        tag_name = self.request.POST.get('name', None)

        if tag_name:

            user_tags = self.request.user.profile.user_tags
            tag, created = user_tags.model.objects.get_or_create(name=tag_name.lower())

            if tag in user_tags.all():
                user_tags.remove(tag)
                message = u'Tog bort bevakning för "{0}"'.format(tag.name)
            else:
                user_tags.add(tag)
                message = u'Du bevakar nu "{0}"'.format(tag.name)

        messages.add_message(self.request, messages.INFO, message)
        referer = self.request.META.get('HTTP_REFERER')
        self.success_url = referer
        return super(ToggleUserTagFormView, self).form_valid(form)

    def form_invalid(self, form):
        for error_message in form.errors['__all__']:
            messages.add_message(self.request, messages.ERROR, error_message)
        referer = self.request.META.get('HTTP_REFERER')
        return redirect(referer)

# OLD STUFF

@never_cache
@login_required()
def read_profile(request, user_id=None):
    """
    Read a profile. Uses the profile of the current user if not given an id.
    
    Note that this takes user id and not profile id. It is good practice to
    never select anything based on profile.
    """
    # Get the user
    if not user_id:
        user = request.user
    else:
        user = User.objects.get(pk=user_id)
    profile, created = Profile.objects.select_related().get_or_create(user=user)
    
    if request.is_ajax():
        template = '_profile.html'
    else:
        template = 'profile.html'
        
    return render(request, template, {"profile": profile,'user':user})
    
@never_cache
@login_required()
def update_profile(request):
    """
    Updates a profile. Users may only update their own profile.
    
    """

    profile, created = Profile.objects.select_related().get_or_create(user=request.user)
    if request.method == 'POST':
        if 'profile-form' in request.POST:
            print 'profile-form'
            form = ProfileForm(request.POST, request.FILES, instance=profile)
            SubscriptionsForm = ProfileSubscriptionsForm(instance=profile)
            
            if form.is_valid():
                form.save()
                
                return HttpResponseRedirect('/user/')
            
        if 'profile-subscriptions-form' in request.POST:            
            form = ProfileForm(instance=profile)
            SubscriptionsForm = ProfileSubscriptionsForm(request.POST, request.FILES, instance=profile)
            
            if SubscriptionsForm.is_valid():
                SubscriptionsForm.save()
                
                return HttpResponseRedirect('/user/')
    else:
        form = ProfileForm(instance=profile)
        SubscriptionsForm = ProfileSubscriptionsForm(instance=profile)

    vars = {
            "profile": profile,
            'user': profile.user,
            'form':form,
            'SubscriptionsForm':SubscriptionsForm,
            }
  
    return render(request, 'update_profile.html', vars)

@never_cache    
@login_required()
def profile_description_form(request,user_id=None):
    user = request.user
    profile, created = Profile.objects.select_related().get_or_create(user=user)
    
    if request.method == 'POST':
        form = ProfileDescriptionForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            
            return HttpResponseRedirect(request.META['HTTP_REFERER'])
    
    action = reverse('ajax_user_description_form', args=[user.id])
    form = ProfileDescriptionForm(instance=profile)
    
    return render(request, 'ajaxform.html', {'form':form,'action':action})

    
        
   