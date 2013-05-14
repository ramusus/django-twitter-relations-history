# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'RelationsHistory'
        db.create_table('twitter_relations_history_relationshistory', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='relations_history', to=orm['twitter_api.User'])),
            ('time', self.gf('django.db.models.fields.DateTimeField')(null=True)),
            ('hidden', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('offset', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('followers_ids', self.gf('picklefield.fields.PickledObjectField')(default=[])),
            ('followers_count', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
        ))
        db.send_create_signal('twitter_relations_history', ['RelationsHistory'])

        # Adding unique constraint on 'RelationsHistory', fields ['user', 'time']
        db.create_unique('twitter_relations_history_relationshistory', ['user_id', 'time'])

        # Adding model 'RelationsHistoryDelta'
        db.create_table('twitter_relations_history_relationshistorydelta', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('history_from', self.gf('django.db.models.fields.related.ForeignKey')(related_name='deltas_from', to=orm['twitter_relations_history.RelationsHistory'])),
            ('history_to', self.gf('django.db.models.fields.related.ForeignKey')(related_name='deltas_to', to=orm['twitter_relations_history.RelationsHistory'])),
            ('followers_left_ids', self.gf('picklefield.fields.PickledObjectField')(default=[])),
            ('followers_entered_ids', self.gf('picklefield.fields.PickledObjectField')(default=[])),
            ('followers_left_count', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('followers_entered_count', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
        ))
        db.send_create_signal('twitter_relations_history', ['RelationsHistoryDelta'])

        # Adding unique constraint on 'RelationsHistoryDelta', fields ['history_from', 'history_to']
        db.create_unique('twitter_relations_history_relationshistorydelta', ['history_from_id', 'history_to_id'])


    def backwards(self, orm):
        # Removing unique constraint on 'RelationsHistoryDelta', fields ['history_from', 'history_to']
        db.delete_unique('twitter_relations_history_relationshistorydelta', ['history_from_id', 'history_to_id'])

        # Removing unique constraint on 'RelationsHistory', fields ['user', 'time']
        db.delete_unique('twitter_relations_history_relationshistory', ['user_id', 'time'])

        # Deleting model 'RelationsHistory'
        db.delete_table('twitter_relations_history_relationshistory')

        # Deleting model 'RelationsHistoryDelta'
        db.delete_table('twitter_relations_history_relationshistorydelta')


    models = {
        'twitter_api.user': {
            'Meta': {'object_name': 'User'},
            'contributors_enabled': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {}),
            'default_profile': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'default_profile_image': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'entities': ('annoying.fields.JSONField', [], {}),
            'favorites_count': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'fetched': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'follow_request_sent': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'followers': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'followings'", 'symmetrical': 'False', 'to': "orm['twitter_api.User']"}),
            'followers_count': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'following': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'friends_count': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'geo_enabled': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.BigIntegerField', [], {'primary_key': 'True'}),
            'is_translator': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'lang': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'listed_count': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'location': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'notifications': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'profile_background_color': ('django.db.models.fields.CharField', [], {'max_length': '6'}),
            'profile_background_image_url': ('django.db.models.fields.URLField', [], {'max_length': '300'}),
            'profile_background_image_url_https': ('django.db.models.fields.URLField', [], {'max_length': '300'}),
            'profile_background_tile': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'profile_banner_url': ('django.db.models.fields.URLField', [], {'max_length': '300'}),
            'profile_image_url': ('django.db.models.fields.URLField', [], {'max_length': '300'}),
            'profile_image_url_https': ('django.db.models.fields.URLField', [], {'max_length': '300'}),
            'profile_link_color': ('django.db.models.fields.CharField', [], {'max_length': '6'}),
            'profile_sidebar_border_color': ('django.db.models.fields.CharField', [], {'max_length': '6'}),
            'profile_sidebar_fill_color': ('django.db.models.fields.CharField', [], {'max_length': '6'}),
            'profile_text_color': ('django.db.models.fields.CharField', [], {'max_length': '6'}),
            'profile_use_background_image': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'protected': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'screen_name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'}),
            'statuses_count': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'time_zone': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '300', 'null': 'True'}),
            'utc_offset': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'verified': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'twitter_relations_history.relationshistory': {
            'Meta': {'ordering': "('user', 'time', '-id')", 'unique_together': "(('user', 'time'),)", 'object_name': 'RelationsHistory'},
            'followers_count': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'followers_ids': ('picklefield.fields.PickledObjectField', [], {'default': '[]'}),
            'hidden': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'offset': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'time': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'relations_history'", 'to': "orm['twitter_api.User']"})
        },
        'twitter_relations_history.relationshistorydelta': {
            'Meta': {'unique_together': "(('history_from', 'history_to'),)", 'object_name': 'RelationsHistoryDelta'},
            'followers_entered_count': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'followers_entered_ids': ('picklefield.fields.PickledObjectField', [], {'default': '[]'}),
            'followers_left_count': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'followers_left_ids': ('picklefield.fields.PickledObjectField', [], {'default': '[]'}),
            'history_from': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'deltas_from'", 'to': "orm['twitter_relations_history.RelationsHistory']"}),
            'history_to': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'deltas_to'", 'to': "orm['twitter_relations_history.RelationsHistory']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        }
    }

    complete_apps = ['twitter_relations_history']