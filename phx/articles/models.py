# -*- coding: utf-8 -*-

import datetime

from django.db import models
from django.contrib.auth.models import User
from django.contrib.humanize.templatetags.humanize import naturalday
from django.utils.text import slugify
from django.core.urlresolvers import reverse
from django.core.urlresolvers import reverse_lazy

from django.template.loader import render_to_string


from mptt.models import MPTTModel
from mptt.models import TreeForeignKey
from mptt.models import TreeManager

from phx import site_strings
from core.managers import TaggableManager
from core.templatetags.entry_tags import render_tag
from core.models import Entry
from tags.models import UserTags
from tags.models import ModTags
# South introspection rule
from south.modelsinspector import add_ignored_fields

try:
    from taggit.managers import TaggableManager
except ImportError:
    pass
else:
    add_ignored_fields(["^taggit\.managers"])


class Article(Entry):
    """
    Articles

    """
    user_tags = models.ManyToManyField(
        UserTags,
        related_name='user_tagged_articles')
    mod_tags = models.ManyToManyField(
        ModTags,
        related_name='mod_tagged_articles')
    title = models.CharField(
        max_length=128,
        verbose_name="Rubrik")
    body = models.TextField(
        max_length=5120,
        verbose_name="Text",
        help_text=site_strings.COMMENT_FORM_HELP_TEXT)
    allow_comments = models.NullBooleanField(
        default=False,
        verbose_name="Tillåt kommentarer")
    slug = models.SlugField(
        unique=True,
        max_length=1028)

    def save(self, **kwargs):
        slug_text = u"{0} av {1} den {2}-{3}".format(
            self.title,
            self.created_by.username,
            self.date_created.date().isoformat(),
            self.id
        )
        self.slug = slugify(slug_text)
        super(Article, self).save()

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('read_article', args=[self.slug])

    def get_perma_url(self):
        return reverse('read_article', args=[self.id])

    class Meta:
        verbose_name = "Artikel"
        verbose_name_plural = "Artiklar"
        get_latest_by = ["-date_created"]
        ordering = ["-date_created"]


class ArticleComment(MPTTModel):
    """ Threaded comments for blog posts """
    post = models.ForeignKey(Article, related_name="comments")
    author = models.CharField(max_length=60)
    created_by = models.ForeignKey(User, related_name="created_%(class)s_entries", blank=True, null=True)
    comment = models.TextField(max_length=5120, help_text=site_strings.COMMENT_FORM_HELP_TEXT, verbose_name="Kommentar")
    added  = models.DateTimeField(default=datetime.datetime.now,blank=True)
    date_last_changed = models.DateTimeField(auto_now=False, blank=True, null=True)
    
    tags = TaggableManager()
    objects = tree = TreeManager()

    # a link to comment that is being replied, if one exists
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children')
    
    class Meta:
        verbose_name = "Artikelkommentar"
        verbose_name_plural = "Artikelkommentarer"

    class MPTTMeta:
        # comments on one level will be ordered by date of creation
        order_insertion_by=['added']
        
    def __unicode__(self):
        return u'Svar på "{0}"'.format( self.post.title )

    @property
    def get_verbose_name(self):
        return self._meta.verbose_name

    @property
    def ajax_editable_fields(self):
        return ["comment"]

    @property
    def is_deleteble(self):
        
        deleteble = False
        
        if self.is_root_node():
            deleteble = True
        
        if not self.is_leaf_node():
            deleteble = False
            
        if not self.is_root_node():
            siblings = self.get_siblings(include_self=True).reverse()
            siblings_count = len (siblings)
            
           # If not alone?
            if siblings_count > 1:
                deleteble = False 

            #If last? 
            if siblings[0] == self:
                deleteble = True

        return deleteble
        
    @property
    def is_editable(self):
        """
        Limit is_editable to one day
        """
        return datetime.datetime.now() - self.added < datetime.timedelta(days=1)
           
    @property
    def allow_history(self):  
        return True    
        
    @property
    def fields_history(self):
        return ["comment"]

    def get_absolute_url(self):
        return "{0}?h=comment-{1}".format( reverse('read_article', args=[self.post.id]), self.id )
        
    @property
    def get_reply_url(self):
        return reverse('comment_article', args=[self.post.id])

class defaultArticleCategories(models.Model):
    """
    Default categories for articles
    using tags
    """
    tags = TaggableManager()

    def __unicode__(self):

        text = self.tags.all()[0]

        return u'%s' % (text)
        

class ModeratorArticleCategories(models.Model):
    """
    Default categories for the articles
    for moderators, using tags
    """
    tags = TaggableManager()

    def __unicode__(self):

        text = self.tags.all()[0]

        return u'%s' % (text)
