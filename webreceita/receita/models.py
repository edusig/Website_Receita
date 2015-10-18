from django.db import models
from choices import COZIMENTO_ESCOLHAS
from django.contrib.localflavor.br.br_states import STATE_CHOICES


class Autor(models.Model):
    nome_completo = models.CharField(max_length=200)
    nascimento = models.DateTimeField()
    cidade = models.CharField(max_length=200)
    estado = models.IntegerField(choices=STATE_CHOICES)
    telefone = models.CharField(max_length=15)
    login = models.EmailField(max_length=200)
    senha = models.CharField(max_length=30)


class Categoria(models.Model):
    nome = models.CharField(max_length=200)


class Receita(models.Model):
    nome = models.CharField(max_length=50)
    descricao = models.TextField(max_length=300)
    autor = models.ForeignKey(Autor)
    categoria = models.ForeignKey(Categoria)
    instrucao = models.TextField(max_length=800)
    porcoes = models.IntegerField()
    valor_nutricional = models.IntegerField()
    metodo_cozimento = models.IntegerField(choices=COZIMENTO_ESCOLHAS, default=1)
    avaliacao = models.IntegerField()

class ReceitaImagem(models.Model):
    image = models.ImageField()
    ref = models.ForeignKey(Receita)


class Ingredientes(models.Model):
    nome = models.CharField(max_length=100)
    quantidade = models.IntegerField()
    unidade = models.CharField(max_length=20)
    receita = models.ForeignKey(Receita)
