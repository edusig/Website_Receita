from django.shortcuts import render_to_response
from django.template import RequestContext
from receita.models import *
from django.contrib.auth import authenticate, login, logout


def index(req):
    cdict = load_menu_sidebar()
    receitas = []
    for cat in cdict['categorias']:
        receitas += [{'Nome': cat.nome, 'categoria': True}]
        receitas = receitas + [{'categoria': False, 'receita': x} for x in Receita.objects.filter(categoria=cat)[:3]]
    cdict.update({'receitas': receitas})
    context = RequestContext(req, cdict)
    return render_to_response('index.html', context)


def login(req):
    cdict = load_menu_sidebar()
    loginresult = None
    if req.method == 'POST':
        username = req.POST['username']
        password = req.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(req, user, 'index.html')
            else:
                loginresult = 'disabled'
        else:
            loginresult = 'invalid'
    cdict.update({'result': loginresult})
    context = RequestContext(req, cdict)
    return render_to_response('login.html', context)


def register(req):
    cdict = load_menu_sidebar()
    context = RequestContext(req, cdict)
    return render_to_response('cadastro.html', context)


def user_logout(req):
    logout(req, 'index.html')


def categoria(req, cat):
    cdict = load_menu_sidebar()
    categoria_select = Categoria.objects.get(nome=cat)
    receitas = Receita.objects.filter(categoria=categoria_select)
    cdict.update({'cat': cat, 'receitas': receitas})
    context = RequestContext(req, cdict)
    return render_to_response('receita_categoria.html', context)


def cadastro_receita(req):
    cdict = load_menu_sidebar()
    context = RequestContext(req, cdict)
    return render_to_response('cadastro_receita.html', context)


def detalhe_receita(req, pk):
    cdict = load_menu_sidebar()
    receita = Receita.objects.get(pk=pk)
    ingredientes = Ingredientes.objects.filter(receita=receita)
    receita.instrucao = receita.instrucao.split('\n')
    receita.metodo_cozimento = COZIMENTO_ESCOLHAS[receita.metodo_cozimento][1]
    bebida = receita.categoria.nome == 'Bebidas'
    cdict.update({'receita': receita, 'ingredientes': ingredientes, 'isbebida': bebida})
    context = RequestContext(req, cdict)
    return render_to_response('receita.html', context)


def receita_do_dia():
    pks = [1]
    return Receita.objects.filter(pk__in=pks)


def top_receitas():
    pks = [3,5,6]
    return Receita.objects.filter(pk__in=pks)


def load_menu_sidebar():
    return {'categorias' : Categoria.objects.all(), 'receita_do_dia': receita_do_dia(), 'top_receitas': top_receitas()}
