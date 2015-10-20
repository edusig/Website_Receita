from django.db import models
from choices import COZIMENTO_ESCOLHAS, STATE_CHOICES


class Autor(models.Model):
    nome_completo = models.CharField(max_length=200)
    nascimento = models.DateTimeField()
    cidade = models.CharField(max_length=200)
    estado = models.CharField(max_length=2, choices=STATE_CHOICES)
    telefone = models.CharField(max_length=15)
    login = models.EmailField(max_length=200)
    senha = models.CharField(max_length=30)
    
    def __unicode__(self):
        return self.nome_completo


class Categoria(models.Model):
    nome = models.CharField(max_length=200)

    def __unicode__(self):
        return self.nome


class Receita(models.Model):
    nome = models.CharField(max_length=50)
    descricao = models.TextField(max_length=300)
    autor = models.ForeignKey(Autor)
    categoria = models.ForeignKey(Categoria)
    instrucao = models.TextField(max_length=800)
    porcoes = models.IntegerField()
    valor_nutricional = models.IntegerField()
    metodo_cozimento = models.IntegerField(choices=COZIMENTO_ESCOLHAS, default=1)
    image = models.ImageField(upload_to="receita_imagens/")
    avaliacao = models.IntegerField()
    
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