# -*- coding: utf-8 -*-

from django.contrib import messages
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required, permission_required
from django.views.decorators.cache import never_cache
from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.core.exceptions import ObjectDoesNotExist

from core.utils import render, validate_internal_tags, get_datatables_records
from django.core.urlresolvers import reverse
from notifications.models import Notification

from .models import Article
from .models import ArticleComment
from .models import defaultArticleCategories
from .forms import DefaultArticleTagsForm
from .forms import ArticleForm
from .forms import ArticleBodyForm
from .forms import ArticleCommentForm


# New stuff
from django.db.models import Count
from django.views.generic import ListView
from django.views.generic import DetailView
from django.views.generic.edit import CreateView
from braces.views import SetHeadlineMixin
from braces.views import LoginRequiredMixin
from braces.views import SelectRelatedMixin
from tags.views import TagSearchMixin
from core.views import ListOrderingMixin
from core.views import ObjectSearchMixin
from tags.models import UserTags
from profiles.forms import SubscribeTagForm


class ArticleListView(ObjectSearchMixin, ListOrderingMixin, TagSearchMixin,
                      SelectRelatedMixin, LoginRequiredMixin,
                      SetHeadlineMixin, ListView):
    search_fields = ['title', 'body']
    search_model = Article
    login_url = "/"
    headline = 'Artiklar'
    queryset = Article.objects.all()
    context_object_name = 'article_list'
    paginate_by = 50
    select_related = [
        'created_by',
        'last_changed_by',
        'deleted_by',
        'user_tags',
        'mod_tags'
    ]

    def get_context_data(self, **kwargs):
        kwargs['main_categories'] = UserTags.objects \
            .filter(main_article_category=True)

        kwargs['top_used_categories'] = UserTags.objects \
            .annotate(articles_count=Count('user_tagged_articles')) \
            .order_by('-articles_count') \
            .exclude(main_article_category=True)[:5]

        kwargs['top_subscribed_categories'] = UserTags.objects \
            .annotate(subscriptions_count=Count('user_subscriptions')) \
            .order_by('-subscriptions_count') \
            .exclude(main_article_category=True)[:5]

        kwargs['user_categories'] = self.request.user.profile.user_tags.all()
        kwargs['subscribe_tag_form'] = SubscribeTagForm()

        active_tags = self.request.GET.get('tags', None)
        if active_tags:
            kwargs['active_tags'] = UserTags.objects.filter(
                name__in=active_tags.split(','))
        return super(ArticleListView, self).get_context_data(**kwargs)


class ArticleDetailView(LoginRequiredMixin, DetailView):
    model = Article


class ArticleCommentCreateView(LoginRequiredMixin, CreateView):
    model = ArticleComment
    fields = ['comment']
    form_class = ArticleCommentForm

    def form_valid(self, form):
        # Attach parent if present
        parent_id = form.data.get('parent', None)
        if parent_id:
            form.instance.parent = ArticleComment.objects.get(id=parent_id)

        # Ownership
        form.instance.created_by = self.request.user
        form.instance.author = self.request.user

        # Attach the post
        post_id = self.kwargs.get('post_pk', False)
        if post_id:
            post = Article.objects.get(id=post_id)
        else:
            post_slug = self.kwargs.get('post_slug', False)
            post = Article.objects.get(slug=post_slug)
        form.instance.post = post
        return super(ArticleCommentCreateView, self).form_valid(form)


# Old stuff

@never_cache
@login_required()
def list_articles_json(request, tags=None, user_id=None):

    if request.is_ajax():

        #initial querySet
        querySet = Article.active.all()

        if tags:
            tags_array = tags.split(",")
            querySet = querySet.filter(tags__name__in=tags_array)
        
        if user_id:         
            querySet = querySet.filter(created_by__id = user_id)

        #columnIndexNameMap is required for correct sorting behavior
        columnIndexNameMap = {
                                0: 'title',
                                1: 'created',
                                2: 'tags',
                                3: 'allow_comments',
                                4: 'id',
                            }

        #call to generic function from utils
        return get_datatables_records(request, querySet, columnIndexNameMap)

    raise Http404 

@never_cache
@login_required()
def create_article(request, tags=None):
    """
    Create article
    
    """
    
    vars = {
        'form':ArticleForm( user=request.user ),
        'tagform' : DefaultArticleTagsForm(),
        'categories':defaultArticleCategories.objects.all(),
        'moderator_categories': ModeratorArticleCategories.objects.all(),
        }
    
    if tags != None:
        initial_tags = tags.split(',')
        vars['tagform'] = DefaultForumTagsForm(initial={'default_tags': initial_tags })
        
    if request.method == 'POST':
        form = ArticleForm(request.POST, user=request.user)
        tagform = DefaultArticleTagsForm(request.POST)
        
        vars['form'] = form
        vars['tagform'] = tagform
        
        if form.is_valid() & tagform.is_valid():

            default_tags = tagform.cleaned_data['default_tags']
            user_tags = form.cleaned_data['tags']
            user_sub_tags = form.cleaned_data['user_tags']

            # Combine and remove doubles
            all_tags = list(set(default_tags + user_tags + user_sub_tags))
            
            # Check if a default tag is present
            if len(default_tags) == 0:
                messages.add_message(request, messages.INFO, 'Du måste välja minst en huvudkategori!')
                return render(request,'create_article.html', {'form': form,'tagform':tagform, 'categories':vars['categories']})

            # Check maximum allowed tags
            if len( all_tags ) > 5:
                messages.add_message(request, messages.INFO, 'Du kan inte välja fler än fem kategorier!')
                return render(request, 'create_article.html', {'form': form,'tagform':tagform, 'categories':vars['categories']})

            post_values = request.POST.copy()
            all_tags = validate_internal_tags(request, all_tags)
            post_values['tags'] = ', '.join(all_tags)
            
            try:
                if post_values['allow_comments'] == "on":
                    post_values['allow_comments'] = True
            except:
                post_values['allow_comments'] = False
                
            form = ArticleForm(post_values, user=request.user)  
            link = form.save()
            
            return HttpResponseRedirect(reverse('read_article', args=[link.id]))
            
    return render(request,'create_article.html', vars)
    
@never_cache
@login_required()
def read_article(request, user_id=None, id=None, slug=None):
    """
    Read article
    
    """
    
    vars = {
        'categories': defaultArticleCategories.objects.all(),
        'commentform': ArticleCommentForm(),
        }
    
    if id is None and slug is None:
        """
        return all articles
        """

        # Tar bara upp notifikationer
        vars['notes'] = request.user.receiver_entries.filter(content_type__model = 'ArticleComment')

        return render(request,'articles.html', vars)
    
    if id:
        vars['article'] = Article.objects.get(id=id)
    if slug:
        vars['article'] = Article.objects.get(slug=slug)

    if vars['article'].allow_comments:
        vars['comments'] = ArticleComment.objects.filter(post=vars['article'])

    if user_id:
        template = "user_article.html"
        vars['user'] = User.objects.get(pk=user_id)
    else:
        template = "article.html"
    
    try:
        article_note = request.user.receiver_entries.filter(content_type__model = 'article', object_id = id)
    except:
        article_note = []
    
    for note in article_note:
        note.delete()

    return render(request,template, vars)

@never_cache
@login_required()
def delete_article(request,id):
    """
    Delete article
    
    """
    vars = {}
    
    return render(request,'article.html', vars)
    

@never_cache
@login_required()
def search_article(request, tags=None, user_id=None):
    """
    Search articles by tags
    
    Lower cap all tags, to its not 
    possible to get INTERNAL TAGS in
    the serach results
    """

    categories = defaultArticleCategories.objects.all()

    tags = [x for x in tags.split(",")]
    

    if user_id and tags:
        #articles = Article.active.filter(tags__name__in=tags, created_by__id = user_id)
        template = 'user_articles.html'
    else:
        template = 'articles.html'
    
    '''
    if tags and not user_id:
        articles = Article.active.filter(tags__name__in=tags)
    else:
        Article.active.all()
    '''
    ''' 
    if len( articles ) < 1:
        messages.add_message(request, messages.INFO, 'Hittade inga artiklar =(')
    
    '''

    vars = {
            #"articles": articles,
            "categories":categories
            }
            
    if user_id:
        vars['user'] = User.objects.get(pk=user_id)
    
    return render(request, template, vars)
    
@never_cache    
@login_required()
def ajax_article_body_form(request,id=None):
    user = request.user
    article = Article.objects.get(id=id)
    
    if request.method == 'POST':
        form = ArticleBodyForm(request.POST, request.FILES, instance=article)
        if form.is_valid():
            form.save()
            
            return read_article(request,id)
    
    action = reverse('ajax_article_body_form', args=[id])
    form = ArticleBodyForm(instance=article)
    
    return render(request, 'ajaxform.html', {'form':form,'action':action})

    
       
@never_cache
@login_required()
def comment_article(request,article_id):
    """
    Comment article
    
    """
    
    post = Article.objects.get(id=article_id)
    
    
    vars = {
        
    }
    
    if request.method == 'POST':
        author = request.user
        form = ArticleCommentForm(request.POST)
        
        if form.is_valid(): 
            comment = ArticleComment(
                post = post,
                created_by = request.user,
                author=author,
                comment=request.POST['comment'],
            )
            
            # if this is a reply to a comment, not to a post
            parent_id = None
            if request.POST['parent_id'] != '':
                parent_id = request.POST['parent_id']
                comment.parent = ArticleComment.objects.get( id = parent_id )
            comment.save()

            # Get instance ids for all siblings
            # if there are any unreplied siblings we need to remove them
            instance_ids = []
            if comment.is_child_node():              
                try:
                    siblings = comment.get_siblings(include_self=False)
                    instance_ids = [sibling.id for sibling in siblings]
                except:
                    pass

            # If this is an answear to an post, include them in the
            # in the instance array for notification remowal
            if parent_id:
                 instance_ids += [parent_id]

            # Remowe notifications
            if instance_ids:
                notes = request.user.receiver_entries.filter(content_type__model = 'articlecomment', object_id__in = instance_ids)
                for note in notes:
                    note.delete()

        if request.is_ajax():
            vars = {
                'comments' : ArticleComment.objects.filter(post__id=article_id),
                'article_id': article_id,
                'commentform': ArticleCommentForm(),
                'app_name': "articles",
                'model_name': "ArticleComment",
                'post_url': reverse('comment_article', args=[article_id]),
                }

            return render(request, '_comments.html', vars )

    return HttpResponseRedirect(reverse('read_article', args=[article_id]))

@never_cache
@login_required()
def ajax_comments_article(request, article_id):
    if request.is_ajax():
        
        vars = {
            'comments' : ArticleComment.objects.filter(post__id=article_id),
            'article_id': article_id,
            'commentform': ArticleCommentForm(),
            'app_name': "articles",
            'model_name': "ArticleComment",
            'post_url': reverse('comment_article', args=[article_id]),
            }

        return render(request, '_article_comments.html', vars )
    raise Http404 