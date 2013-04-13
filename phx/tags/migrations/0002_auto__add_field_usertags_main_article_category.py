# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'UserTags.main_article_category'
        db.add_column(u'tags_usertags', 'main_article_category',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'UserTags.main_article_category'
        db.delete_column(u'tags_usertags', 'main_article_category')


    models = {
        u'tags.modtags': {
            'Meta': {'object_name': 'ModTags'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'tags.usertags': {
            'Meta': {'object_name': 'UserTags'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'main_article_category': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        }
    }

    complete_apps = ['tags']