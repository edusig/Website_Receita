# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'PerfilUsuario'
        db.create_table('receita_perfilusuario', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('nome_completo', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('nascimento', self.gf('django.db.models.fields.DateField')()),
            ('cidade', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('estado', self.gf('django.db.models.fields.CharField')(max_length=2)),
            ('telefone', self.gf('django.db.models.fields.CharField')(max_length=15)),
            ('usuario', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], unique=True)),
        ))
        db.send_create_signal('receita', ['PerfilUsuario'])

        # Adding model 'Categoria'
        db.create_table('receita_categoria', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('nome', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal('receita', ['Categoria'])

        # Adding model 'Receita'
        db.create_table('receita_receita', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('nome', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('descricao', self.gf('django.db.models.fields.TextField')(max_length=300)),
            ('autor', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['receita.PerfilUsuario'])),
            ('categoria', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['receita.Categoria'])),
            ('instrucao', self.gf('django.db.models.fields.TextField')(max_length=800)),
            ('porcoes', self.gf('django.db.models.fields.IntegerField')()),
            ('valor_nutricional', self.gf('django.db.models.fields.IntegerField')()),
            ('metodo_preparo', self.gf('django.db.models.fields.IntegerField')(default=1)),
            ('image', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
        ))
        db.send_create_signal('receita', ['Receita'])

        # Adding model 'ReceitaImagem'
        db.create_table('receita_receitaimagem', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('image', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
            ('ref', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['receita.Receita'])),
        ))
        db.send_create_signal('receita', ['ReceitaImagem'])

        # Adding model 'Ingredientes'
        db.create_table('receita_ingredientes', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('nome', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('quantidade', self.gf('django.db.models.fields.FloatField')()),
            ('unidade', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('receita', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['receita.Receita'])),
        ))
        db.send_create_signal('receita', ['Ingredientes'])

        # Adding model 'Comentario'
        db.create_table('receita_comentario', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('comentario', self.gf('django.db.models.fields.TextField')(max_length=1000)),
            ('nome', self.gf('django.db.models.fields.CharField')(default=None, max_length=200)),
            ('usuario', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('receita', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['receita.Receita'])),
        ))
        db.send_create_signal('receita', ['Comentario'])

        # Adding model 'Voto'
        db.create_table('receita_voto', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('valor', self.gf('django.db.models.fields.IntegerField')(default=1)),
            ('usuario', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['receita.PerfilUsuario'])),
            ('receita', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['receita.Receita'])),
        ))
        db.send_create_signal('receita', ['Voto'])


    def backwards(self, orm):
        # Deleting model 'PerfilUsuario'
        db.delete_table('receita_perfilusuario')

        # Deleting model 'Categoria'
        db.delete_table('receita_categoria')

        # Deleting model 'Receita'
        db.delete_table('receita_receita')

        # Deleting model 'ReceitaImagem'
        db.delete_table('receita_receitaimagem')

        # Deleting model 'Ingredientes'
        db.delete_table('receita_ingredientes')

        # Deleting model 'Comentario'
        db.delete_table('receita_comentario')

        # Deleting model 'Voto'
        db.delete_table('receita_voto')


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
        'receita.categoria': {
            'Meta': {'object_name': 'Categoria'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nome': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        'receita.comentario': {
            'Meta': {'object_name': 'Comentario'},
            'comentario': ('django.db.models.fields.TextField', [], {'max_length': '1000'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nome': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '200'}),
            'receita': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['receita.Receita']"}),
            'usuario': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'receita.ingredientes': {
            'Meta': {'object_name': 'Ingredientes'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nome': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'quantidade': ('django.db.models.fields.FloatField', [], {}),
            'receita': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['receita.Receita']"}),
            'unidade': ('django.db.models.fields.CharField', [], {'max_length': '20'})
        },
        'receita.perfilusuario': {
            'Meta': {'object_name': 'PerfilUsuario'},
            'cidade': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'estado': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nascimento': ('django.db.models.fields.DateField', [], {}),
            'nome_completo': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'telefone': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'usuario': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'unique': 'True'})
        },
        'receita.receita': {
            'Meta': {'object_name': 'Receita'},
            'autor': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['receita.PerfilUsuario']"}),
            'categoria': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['receita.Categoria']"}),
            'descricao': ('django.db.models.fields.TextField', [], {'max_length': '300'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'instrucao': ('django.db.models.fields.TextField', [], {'max_length': '800'}),
            'metodo_preparo': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'nome': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'porcoes': ('django.db.models.fields.IntegerField', [], {}),
            'valor_nutricional': ('django.db.models.fields.IntegerField', [], {})
        },
        'receita.receitaimagem': {
            'Meta': {'object_name': 'ReceitaImagem'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'ref': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['receita.Receita']"})
        },
        'receita.voto': {
            'Meta': {'object_name': 'Voto'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'receita': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['receita.Receita']"}),
            'usuario': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['receita.PerfilUsuario']"}),
            'valor': ('django.db.models.fields.IntegerField', [], {'default': '1'})
        }
    }

    complete_apps = ['receita']