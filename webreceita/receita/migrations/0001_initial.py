# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Autor'
        db.create_table('receita_autor', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('nome_completo', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('nascimento', self.gf('django.db.models.fields.DateTimeField')()),
            ('cidade', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('estado', self.gf('django.db.models.fields.CharField')(max_length=2)),
            ('telefone', self.gf('django.db.models.fields.CharField')(max_length=15)),
            ('login', self.gf('django.db.models.fields.EmailField')(max_length=200)),
            ('senha', self.gf('django.db.models.fields.CharField')(max_length=30)),
        ))
        db.send_create_signal('receita', ['Autor'])

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
            ('autor', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['receita.Autor'])),
            ('categoria', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['receita.Categoria'])),
            ('instrucao', self.gf('django.db.models.fields.TextField')(max_length=800)),
            ('porcoes', self.gf('django.db.models.fields.IntegerField')()),
            ('valor_nutricional', self.gf('django.db.models.fields.IntegerField')()),
            ('metodo_cozimento', self.gf('django.db.models.fields.IntegerField')(default=1)),
            ('image', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
            ('avaliacao', self.gf('django.db.models.fields.IntegerField')()),
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
            ('quantidade', self.gf('django.db.models.fields.IntegerField')()),
            ('unidade', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('receita', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['receita.Receita'])),
        ))
        db.send_create_signal('receita', ['Ingredientes'])


    def backwards(self, orm):
        # Deleting model 'Autor'
        db.delete_table('receita_autor')

        # Deleting model 'Categoria'
        db.delete_table('receita_categoria')

        # Deleting model 'Receita'
        db.delete_table('receita_receita')

        # Deleting model 'ReceitaImagem'
        db.delete_table('receita_receitaimagem')

        # Deleting model 'Ingredientes'
        db.delete_table('receita_ingredientes')


    models = {
        'receita.autor': {
            'Meta': {'object_name': 'Autor'},
            'cidade': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'estado': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'login': ('django.db.models.fields.EmailField', [], {'max_length': '200'}),
            'nascimento': ('django.db.models.fields.DateTimeField', [], {}),
            'nome_completo': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'senha': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'telefone': ('django.db.models.fields.CharField', [], {'max_length': '15'})
        },
        'receita.categoria': {
            'Meta': {'object_name': 'Categoria'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nome': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        'receita.ingredientes': {
            'Meta': {'object_name': 'Ingredientes'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nome': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'quantidade': ('django.db.models.fields.IntegerField', [], {}),
            'receita': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['receita.Receita']"}),
            'unidade': ('django.db.models.fields.CharField', [], {'max_length': '20'})
        },
        'receita.receita': {
            'Meta': {'object_name': 'Receita'},
            'autor': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['receita.Autor']"}),
            'avaliacao': ('django.db.models.fields.IntegerField', [], {}),
            'categoria': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['receita.Categoria']"}),
            'descricao': ('django.db.models.fields.TextField', [], {'max_length': '300'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'instrucao': ('django.db.models.fields.TextField', [], {'max_length': '800'}),
            'metodo_cozimento': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'nome': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'porcoes': ('django.db.models.fields.IntegerField', [], {}),
            'valor_nutricional': ('django.db.models.fields.IntegerField', [], {})
        },
        'receita.receitaimagem': {
            'Meta': {'object_name': 'ReceitaImagem'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'ref': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['receita.Receita']"})
        }
    }

    complete_apps = ['receita']