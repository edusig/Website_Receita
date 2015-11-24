from django.db import models
from django.contrib.auth.models import User
from choices import PREPARO_ESCOLHAS, STATE_CHOICES


class PerfilUsuario(models.Model):
    nome_completo = models.CharField(max_length=200)
    nascimento = models.DateField()
    cidade = models.CharField(max_length=200)
    estado = models.CharField(max_length=2, choices=STATE_CHOICES)
    telefone = models.CharField(max_length=15)
    usuario = models.ForeignKey(User, unique=True)
    
    def __unicode__(self):
        return self.nome_completo


class Categoria(models.Model):
    nome = models.CharField(max_length=200)

    def __unicode__(self):
        return self.nome


class Receita(models.Model):
    nome = models.CharField(max_length=50)
    descricao = models.TextField(max_length=300)
    autor = models.ForeignKey(PerfilUsuario)
    categoria = models.ForeignKey(Categoria)
    instrucao = models.TextField(max_length=800)
    porcoes = models.IntegerField()
    valor_nutricional = models.IntegerField()
    metodo_preparo = models.IntegerField(choices=PREPARO_ESCOLHAS, default=1)
    image = models.ImageField(upload_to="receita_imagens/")
    
    def __unicode__(self):
        return self.nome


class ReceitaImagem(models.Model):
    image = models.ImageField(upload_to="receita_imagens/")
    ref = models.ForeignKey(Receita)

    def __unicode__(self):
        return self.image.name


class Ingredientes(models.Model):
    nome = models.CharField(max_length=100)
    quantidade = models.FloatField()
    unidade = models.CharField(max_length=20)
    receita = models.ForeignKey(Receita)

    def __unicode__(self):
        return self.nome


class Comentario(models.Model):
    comentario = models.TextField(max_length=1000)
    usuario = models.ForeignKey(User)
    receita = models.ForeignKey(Receita)

    def __unicode__(self):
        return "{}".format(self.comentario)


class Voto(models.Model):
    valor = models.IntegerField(default=1)
    usuario = models.ForeignKey(User)
    receita = models.ForeignKey(Receita)

    def __unicode__(self):
        return self.valor
