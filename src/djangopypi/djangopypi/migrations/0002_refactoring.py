# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):
    
    def forwards(self, orm):
        
        # Adding model 'File'
        db.create_table('djangopypi_file', (
            ('comment', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('md5_digest', self.gf('django.db.models.fields.CharField')(max_length=32, blank=True)),
            ('filetype', self.gf('django.db.models.fields.CharField')(max_length=32)),
            ('pyversion', self.gf('django.db.models.fields.CharField')(max_length=16, blank=True)),
            ('uploader', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('signature', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('release', self.gf('django.db.models.fields.related.ForeignKey')(related_name='files', to=orm['djangopypi.Release'])),
            ('distribution', self.gf('django.db.models.fields.files.FileField')(max_length=100)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('djangopypi', ['File'])

        # Adding model 'Review'
        db.create_table('djangopypi_review', (
            ('release', self.gf('django.db.models.fields.related.ForeignKey')(related_name='reviews', to=orm['djangopypi.Release'])),
            ('rating', self.gf('django.db.models.fields.PositiveSmallIntegerField')(blank=True)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('comment', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal('djangopypi', ['Review'])

        db.delete_column('djangopypi_project', 'license')
        db.delete_column('djangopypi_project', 'updated')
        db.delete_column('djangopypi_project', 'metadata_version')
        db.delete_column('djangopypi_project', 'author')
        db.delete_column('djangopypi_project', 'home_page')
        db.delete_column('djangopypi_project', 'download_url')
        db.delete_column('djangopypi_project', 'summary')
        db.delete_column('djangopypi_project', 'author_email')
        db.delete_column('djangopypi_project', 'owner_id')
        db.delete_column('djangopypi_project', 'id')
        db.delete_column('djangopypi_project', 'description')

        db.add_column('djangopypi_project', 'auto_hide', self.gf('django.db.models.fields.BooleanField')(default=True, blank=True), keep_default=False)
        db.add_column('djangopypi_project', 'allow_comments', self.gf('django.db.models.fields.BooleanField')(default=True, blank=True), keep_default=False)
        
        db.alter_column('djangopypi_project', 'name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255, primary_key=True))

        db.delete_table('djangopypi_project_classifiers')

        # Adding M2M table for field owners on 'Project'
        db.create_table('djangopypi_project_owners', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('project', models.ForeignKey(orm['djangopypi.project'], null=False)),
            ('user', models.ForeignKey(orm['auth.user'], null=False))
        ))
        db.create_unique('djangopypi_project_owners', ['project_id', 'user_id'])

        # Adding M2M table for field maintainers on 'Project'
        db.create_table('djangopypi_project_maintainers', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('project', models.ForeignKey(orm['djangopypi.project'], null=False)),
            ('user', models.ForeignKey(orm['auth.user'], null=False))
        ))
        db.create_unique('djangopypi_project_maintainers', ['project_id', 'user_id'])

        

        # Deleting field 'Release.upload_time'
        db.delete_column('djangopypi_release', 'upload_time')

        # Deleting field 'Release.md5_digest'
        db.delete_column('djangopypi_release', 'md5_digest')

        # Deleting field 'Release.filetype'
        db.delete_column('djangopypi_release', 'filetype')

        # Deleting field 'Release.pyversion'
        db.delete_column('djangopypi_release', 'pyversion')

        # Deleting field 'Release.platform'
        db.delete_column('djangopypi_release', 'platform')

        # Deleting field 'Release.signature'
        db.delete_column('djangopypi_release', 'signature')

        # Deleting field 'Release.distribution'
        db.delete_column('djangopypi_release', 'distribution')

        # Adding field 'Release.metadata_version'
        db.add_column('djangopypi_release', 'metadata_version', self.gf('django.db.models.fields.CharField')(default='1.0', max_length=64), keep_default=False)

        # Adding field 'Release.created'
        db.add_column('djangopypi_release', 'created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, default='', blank=True), keep_default=False)

        # Adding field 'Release.package_info'
        db.add_column('djangopypi_release', 'package_info', self.gf('django.db.models.fields.TextField')(default=''), keep_default=False)
        
        # Adding field 'Release.hidden'
        db.add_column('djangopypi_release', 'hidden', self.gf('django.db.models.fields.BooleanField')(default=False, blank=True), keep_default=False)

        # Removing unique constraint on 'Release', fields ['project', 'platform', 'distribution', 'version', 'pyversion']
        db.delete_unique('djangopypi_release', ['project_id', 'platform', 'distribution', 'version', 'pyversion'])

        # Adding unique constraint on 'Release', fields ['project', 'version']
        db.create_unique('djangopypi_release', ['project_id', 'version'])
    
    
    def backwards(self, orm):
        
        # Deleting model 'File'
        db.delete_table('djangopypi_file')

        # Deleting model 'Review'
        db.delete_table('djangopypi_review')

        # Adding field 'Project.license'
        db.add_column('djangopypi_project', 'license', self.gf('django.db.models.fields.TextField')(default='', blank=True), keep_default=False)

        # Adding field 'Project.updated'
        db.add_column('djangopypi_project', 'updated', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, default='', blank=True), keep_default=False)

        # Adding field 'Project.metadata_version'
        db.add_column('djangopypi_project', 'metadata_version', self.gf('django.db.models.fields.CharField')(default=1.0, max_length=64), keep_default=False)

        # Adding field 'Project.author'
        db.add_column('djangopypi_project', 'author', self.gf('django.db.models.fields.CharField')(default='', max_length=128, blank=True), keep_default=False)

        # Adding field 'Project.home_page'
        db.add_column('djangopypi_project', 'home_page', self.gf('django.db.models.fields.URLField')(max_length=200, null=True, blank=True), keep_default=False)

        # Adding field 'Project.download_url'
        db.add_column('djangopypi_project', 'download_url', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True), keep_default=False)

        # Adding field 'Project.summary'
        db.add_column('djangopypi_project', 'summary', self.gf('django.db.models.fields.TextField')(default='', blank=True), keep_default=False)

        # Adding field 'Project.author_email'
        db.add_column('djangopypi_project', 'author_email', self.gf('django.db.models.fields.CharField')(default='', max_length=255, blank=True), keep_default=False)

        # Adding field 'Project.owner'
        db.add_column('djangopypi_project', 'owner', self.gf('django.db.models.fields.related.ForeignKey')(default='', related_name='projects', to=orm['auth.User']), keep_default=False)

        # Adding field 'Project.id'
        db.add_column('djangopypi_project', 'id', self.gf('django.db.models.fields.AutoField')(default='', primary_key=True), keep_default=False)

        # Adding field 'Project.description'
        db.add_column('djangopypi_project', 'description', self.gf('django.db.models.fields.TextField')(default='', blank=True), keep_default=False)

        # Deleting field 'Project.auto_hide'
        db.delete_column('djangopypi_project', 'auto_hide')

        # Deleting field 'Project.allow_comments'
        db.delete_column('djangopypi_project', 'allow_comments')

        # Adding M2M table for field classifiers on 'Project'
        db.create_table('djangopypi_project_classifiers', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('project', models.ForeignKey(orm['djangopypi.project'], null=False)),
            ('classifier', models.ForeignKey(orm['djangopypi.classifier'], null=False))
        ))
        db.create_unique('djangopypi_project_classifiers', ['project_id', 'classifier_id'])

        # Removing M2M table for field owners on 'Project'
        db.delete_table('djangopypi_project_owners')

        # Removing M2M table for field maintainers on 'Project'
        db.delete_table('djangopypi_project_maintainers')

        # Changing field 'Project.name'
        db.alter_column('djangopypi_project', 'name', self.gf('django.db.models.fields.CharField')(max_length=255, unique=True))

        # Adding field 'Release.upload_time'
        db.add_column('djangopypi_release', 'upload_time', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, default='', blank=True), keep_default=False)

        # Adding field 'Release.md5_digest'
        db.add_column('djangopypi_release', 'md5_digest', self.gf('django.db.models.fields.CharField')(default='', max_length=255, blank=True), keep_default=False)

        # Adding field 'Release.filetype'
        db.add_column('djangopypi_release', 'filetype', self.gf('django.db.models.fields.CharField')(default='', max_length=255, blank=True), keep_default=False)

        # Adding field 'Release.pyversion'
        db.add_column('djangopypi_release', 'pyversion', self.gf('django.db.models.fields.CharField')(default='', max_length=255, blank=True), keep_default=False)

        # Adding field 'Release.platform'
        db.add_column('djangopypi_release', 'platform', self.gf('django.db.models.fields.CharField')(default='', max_length=255, blank=True), keep_default=False)

        # Adding field 'Release.signature'
        db.add_column('djangopypi_release', 'signature', self.gf('django.db.models.fields.CharField')(default='', max_length=128, blank=True), keep_default=False)

        # Adding field 'Release.distribution'
        db.add_column('djangopypi_release', 'distribution', self.gf('django.db.models.fields.files.FileField')(default='', max_length=100), keep_default=False)

        # Deleting field 'Release.metadata_version'
        db.delete_column('djangopypi_release', 'metadata_version')

        # Deleting field 'Release.created'
        db.delete_column('djangopypi_release', 'created')

        # Deleting field 'Release.package_info'
        db.delete_column('djangopypi_release', 'package_info')
        
        # Deleting field 'Release.package_info'
        db.delete_column('djangopypi_release', 'hidden')

        # Adding unique constraint on 'Release', fields ['project', 'platform', 'distribution', 'version', 'pyversion']
        db.create_unique('djangopypi_release', ['project_id', 'platform', 'distribution', 'version', 'pyversion'])

        # Removing unique constraint on 'Release', fields ['project', 'version']
        db.delete_unique('djangopypi_release', ['project_id', 'version'])
    
    
    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
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
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'djangopypi.classifier': {
            'Meta': {'object_name': 'Classifier'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'})
        },
        'djangopypi.file': {
            'Meta': {'unique_together': "(('release', 'filetype', 'pyversion'),)", 'object_name': 'File'},
            'comment': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'distribution': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'filetype': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'md5_digest': ('django.db.models.fields.CharField', [], {'max_length': '32', 'blank': 'True'}),
            'pyversion': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'release': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'files'", 'to': "orm['djangopypi.Release']"}),
            'signature': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'uploader': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'djangopypi.project': {
            'Meta': {'object_name': 'Project'},
            'allow_comments': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'auto_hide': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'maintainers': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'projects_maintained'", 'to': "orm['auth.User']"}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255', 'primary_key': 'True'}),
            'owners': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'projects_owned'", 'to': "orm['auth.User']"})
        },
        'djangopypi.release': {
            'Meta': {'unique_together': "(('project', 'version'),)", 'object_name': 'Release'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'metadata_version': ('django.db.models.fields.CharField', [], {'default': "'1.0'", 'max_length': '64'}),
            'package_info': ('django.db.models.fields.TextField', [], {}),
            'hidden': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'releases'", 'to': "orm['djangopypi.Project']"}),
            'version': ('django.db.models.fields.CharField', [], {'max_length': '128'})
        },
        'djangopypi.review': {
            'Meta': {'object_name': 'Review'},
            'comment': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'rating': ('django.db.models.fields.PositiveSmallIntegerField', [], {'blank': 'True'}),
            'release': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'reviews'", 'to': "orm['djangopypi.Release']"})
        }
    }
    
    complete_apps = ['djangopypi']
