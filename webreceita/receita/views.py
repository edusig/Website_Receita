from django.shortcuts import render_to_response
from django.template import RequestContext
from receita.models import *


def index(req):
    categorias = Categoria.objects.all()
    receitas = []
    for cat in categorias:
        receitas += [{'Nome': cat.nome, 'categoria': True}]
        receitas = receitas + [{'categoria': False, 'receita': x} for x in Receita.objects.filter(categoria=cat)[:3]]
    context = RequestContext(req, {'categorias': categorias, 'receitas': receitas, 'receita_do_dia': receita_do_dia(), 'top_receitas': top_receitas()})
    print(receitas)
    return render_to_response('index.html', context)


def login(req):
    categorias = Categoria.objects.all()
    context = RequestContext(req, {'categorias':categorias, 'receita_do_dia': receita_do_dia(), 'top_receitas': top_receitas()})
    return render_to_response('login.html', context)


def register(req):
    categorias = Categoria.objects.all()
    context = RequestContext(req, {'categorias':categorias, 'receita_do_dia': receita_do_dia(), 'top_receitas': top_receitas()})
    return render_to_response('cadastro.html', context)


def categoria(req, cat):
    categorias = Categoria.objects.all()
    categoria_select = Categoria.objects.get(nome=cat)
    receitas = Receita.objects.filter(categoria=categoria_select)
    context = RequestContext(req, {'categorias': categorias, 'cat': cat, 'receitas': receitas, 'receita_do_dia': receita_do_dia(), 'top_receitas': top_receitas()})
    return render_to_response('receita_categoria.html', context)


def cadastro_receita(req):
    categorias = Categoria.objects.all()
    context = RequestContext(req, {'categorias':categorias, 'receita_do_dia': receita_do_dia(), 'top_receitas': top_receitas()})
    return render_to_response('cadastro_receita.html', context)


def detalhe_receita(req, pk):
    categorias = Categoria.objects.all()
    receita = Receita.objects.get(pk=pk)
    ingredientes = Ingredientes.objects.filter(receita=receita)
    receita.instrucao = receita.instrucao.split('\n')
    receita.metodo_cozimento = COZIMENTO_ESCOLHAS[receita.metodo_cozimento][1]
    bebida = receita.categoria.nome == 'Bebidas'
    context = RequestContext(req, {'categorias': categorias, 'receita': receita, 'ingredientes': ingredientes, 'isbebida': bebida, 'receita_do_dia': receita_do_dia(), 'top_receitas': top_receitas()})
    return render_to_response('receita.html', context)


def receita_do_dia():
    pks = [1]
    return Receita.objects.filter(pk__in=pks)


def top_receitas():
    pks = [3,5,6]
    return Receita.objects.filter(pk__in=pks)

