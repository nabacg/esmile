# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Joke'
        db.create_table('jokeserver_joke', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('value', self.gf('django.db.models.fields.TextField')()),
            ('owner', self.gf('django.db.models.fields.related.ForeignKey')(related_name='jokes', to=orm['auth.User'])),
            ('date_created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('date_last_update', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('sent', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('jokeserver', ['Joke'])

        # Adding model 'Subscriber'
        db.create_table('jokeserver_subscriber', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('teller', self.gf('django.db.models.fields.related.ForeignKey')(related_name='joke_listeners', to=orm['auth.User'])),
            ('listener', self.gf('django.db.models.fields.related.ForeignKey')(related_name='joke_tellers', to=orm['auth.User'])),
            ('date_assigned', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('jokeserver', ['Subscriber'])

        # Adding model 'ReceivedJoke'
        db.create_table('jokeserver_receivedjoke', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('subscriber', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['jokeserver.Subscriber'])),
            ('joke', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['jokeserver.Joke'])),
            ('send', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('like_id', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('date_send', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal('jokeserver', ['ReceivedJoke'])


    def backwards(self, orm):
        
        # Deleting model 'Joke'
        db.delete_table('jokeserver_joke')

        # Deleting model 'Subscriber'
        db.delete_table('jokeserver_subscriber')

        # Deleting model 'ReceivedJoke'
        db.delete_table('jokeserver_receivedjoke')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'jokeserver.joke': {
            'Meta': {'object_name': 'Joke'},
            'date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_last_update': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'jokes'", 'to': "orm['auth.User']"}),
            'sent': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'value': ('django.db.models.fields.TextField', [], {})
        },
        'jokeserver.receivedjoke': {
            'Meta': {'object_name': 'ReceivedJoke'},
            'date_send': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'joke': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['jokeserver.Joke']"}),
            'like_id': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'send': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'subscriber': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['jokeserver.Subscriber']"})
        },
        'jokeserver.subscriber': {
            'Meta': {'object_name': 'Subscriber'},
            'date_assigned': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'listener': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'joke_tellers'", 'to': "orm['auth.User']"}),
            'received_jokes': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['jokeserver.Joke']", 'through': "orm['jokeserver.ReceivedJoke']", 'symmetrical': 'False'}),
            'teller': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'joke_listeners'", 'to': "orm['auth.User']"})
        }
    }

    complete_apps = ['jokeserver']
