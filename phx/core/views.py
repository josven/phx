# -*- coding: utf-8 -*-
import datetime
import operator

from django.core.urlresolvers import reverse
from django.utils import simplejson
from django.db.models import Q
from django.db.models import get_model
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.cache import never_cache
from core.utils import render
from forms import update_entry_form, delete_entry_form, subscribe_tag_form
from django.shortcuts import redirect
from reversion.models import Version


class ListOrderingMixin(object):
    """
    Order on ID descending or ID ascending
    """

    def get_queryset(self):
        queryset = super(ListOrderingMixin, self).get_queryset()
        ordering = self.request.GET.get('order', 'no_ordering')

        if ordering == 'descending':
            return queryset.order_by('-id')

        if ordering == 'ascending':
            return queryset.order_by('id')

        # no_ordering
        return queryset


class ObjectSearchMixin(object):
    """
    Simple search in object fields

    """

    search_fields = []
    search_model = None

    def get_queryset(self):
        queryset = super(ObjectSearchMixin, self).get_queryset()
        query_param = self.request.GET.get('q', None)

        if query_param is None:
            return queryset

        query_list = []
        for search_field in self.search_fields:
            keyword = u'{0}__icontains'.format(search_field)
            param = {keyword:query_param}
            query_list.append(Q(**param))

        return queryset.filter(reduce(operator.or_, query_list))
        

# old stuff




@never_cache
@login_required()
def subscribe_tag(request):
    print request.method
    if request.method == 'POST':
        if request.is_ajax():
            form = subscribe_tag_form(request.POST)
            if form.is_valid():
                #Get user
                user = request.user
                profile = request.user.get_profile()
                new_tag = unicode(form.cleaned_data['tag'])
                usertags =  [tag.name for tag in profile.subscriptions.all()]
                if new_tag in usertags:
                    profile.subscriptions.remove(new_tag)
                    data = {
                            'tag_status':0,
                            'message': u'Tog bort bevakning för "{0}"'.format(new_tag)
                            }
                else:
                    profile.subscriptions.add(new_tag)
                    data = {
                            'tag_status':1,
                            'message': u'Du bevakar nu "{0}"'.format(new_tag)
                            }             
                
                return HttpResponse(simplejson.dumps(data), content_type="application/json")
    
    return HttpResponse(status=404)

@never_cache
@login_required()
def preview(request):
    if request.method == 'POST':

        if request.is_ajax():
            preview_id = request.POST.get('preview', None)
                
            if preview_id:
                preview = request.POST.get(preview_id.strip(), None)
                
                if preview:
                    return render(request, 'preview.html', {'preview':preview} )

    return HttpResponse(status=404)
    
@never_cache
@login_required()   
def update_entry(request, app_label, class_name, id):   
    vars = {}

    # Check if theres an valid instance
    try:
        model = get_model(app_label, class_name)
        if model:
            instance = model.objects.get(id=id)
    except ObjectDoesNotExist:
        return HttpResponse(status=404) # No valid instance
        
    # Check if user can edit instance
    if instance.created_by != request.user:
        HttpResponse(status=401) # User not auth
        
        
    # if there any fields to edit
    if not instance.ajax_editable_fields:
        return HttpResponse(status=404) # No field to edit

    
    if request.method == 'GET':

        # Get form
        fields = instance.ajax_editable_fields
        form = update_entry_form( fields, model, instance=instance)
        vars['instance'] = instance
        vars['fields'] = fields
        vars['form'] = form
        vars['action'] = reverse('update_entry', args=[app_label, class_name, id])
    
    if request.method == 'POST':
        fields = instance.ajax_editable_fields
        form = update_entry_form( fields, model, request.POST, instance=instance)

        if form.is_valid():
            form.save()
            
            instance.date_last_changed = datetime.datetime.now()
            instance.save()

            vars['instance'] = instance
            for field in fields:
                vars[field] = getattr(instance,field)
            if request.is_ajax():
                return render(request, 'update_entry_form.html', vars ) 
            return redirect( request.META['HTTP_REFERER'] )
        return HttpResponse(status=401)
        
        
    return render(request, 'update_entry_form.html', vars ) 
    
@never_cache
@login_required()   
def delete_entry(request, app_label, class_name, id):   
    vars = {}

    # Check if theres an valid instance
    try:
        model = get_model(app_label, class_name)
        if model:
            instance = model.objects.get(id=id)
    except ObjectDoesNotExist:
        return HttpResponse(status=404) # No valid instance
        
    # Check if user can delete instance
    if instance.created_by != request.user and instance.is_deleteble:
        HttpResponse(status=401) # User not auth

    if request.method == 'GET':
        # Get form
        form = delete_entry_form()
        vars['form'] = form
    
    if request.method == 'POST':
        form = delete_entry_form( request.POST )
        
        if form.is_valid():
            instance.delete()            
            return HttpResponse(status=200)
        
        return HttpResponse(status=428)
        
        
    return render(request, 'update_entry_form.html', vars )

@never_cache
@login_required()   
def history_entry(request, app_label, class_name, id):   
    vars = {}

    # Check if theres an valid instance
    try:
        model = get_model(app_label, class_name)
        if model:
            instance = model.objects.get(id=id)
    except ObjectDoesNotExist:
        return HttpResponse(status=404) # No valid instance
        
    # Check if history is allowed
    if instance.allow_history and instance.fields_history:
        versions = Version.objects.get_for_object(instance)
        history_diff = []
        for version in versions:
            for field in instance.fields_history:
                history = version.field_dict.get(field, None)
                current = instance.__dict__.get(field, None)
                if history != current:
                    history_diff += [{'content':history,'date':version.revision.date_created}]

        
        vars['history'] = history_diff #versions #Version.objects.get_for_object(instance)
    else:
        return HttpResponse(status=401) # Not allowed
        
    return render(request, 'history_entry_template.html', vars )