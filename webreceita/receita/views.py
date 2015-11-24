from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import authenticate, login, logout
from receita.models import *
from .forms import AutorCadastro, LoginForm, ReceitaCadastro, ComentarForm, AccountForm
import json


def notificacao_index(modifier, cdict):

    notificacoes = {
        'registrado': {
            'msg': "Conta cadastrada com sucesso!",
            'type': "success",
        }
    }

    cdict.update({'notificacao': notificacoes[modifier]})
    return cdict


def do_login(req):
    username = req.POST['username']
    password = req.POST['password']
    try:
        u = User.objects.get(email=username)
        user = authenticate(username=u.username, password=password)
    except User.DoesNotExist:
        user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            login(req, user)
            loginresult = 'ok'
        else:
            loginresult = 'disabled'
    else:
        loginresult = 'invalid'
    return loginresult


def index(req):
    cdict = load_menu_sidebar()
    receitas = []
    for cat in cdict['categorias']:
        receitas += [{'Nome': cat.nome, 'categoria': True}]
        ct = Receita.objects.filter(categoria=cat)[:3]
        receitas = receitas + [{'categoria': False, 'receita': x} for x in ct]
    cdict.update({'receitas': receitas, 'cat': 'home'})
    context = RequestContext(req, cdict)
    return render_to_response('index.html', context)


def index_not(req, notificacao):
    cdict = load_menu_sidebar()
    receitas = []
    for cat in cdict['categorias']:
        receitas += [{'Nome': cat.nome, 'categoria': True}]
        ct = Receita.objects.filter(categoria=cat)[:3]
        receitas = receitas + [{'categoria': False, 'receita': x} for x in ct]
    cdict.update({'receitas': receitas, 'cat': 'home'})
    cdict = notificacao_index(notificacao, cdict)
    context = RequestContext(req, cdict)
    return render_to_response('index.html', context)


def userlogin(req):
    cdict = load_menu_sidebar()
    loginresult = None
    if req.method == 'POST':
        loginresult = do_login(req)
        if loginresult == 'ok':
            return HttpResponseRedirect('/')

    cdict.update({'result': loginresult, 'login_form': LoginForm()})
    context = RequestContext(req, cdict)
    return render_to_response('login.html', context)


def register(req):
    register_form = AutorCadastro()
    user_form = AccountForm()
    if req.user.is_authenticated():
        return HttpResponseRedirect('/')
    elif req.method == 'POST':
        register_form = AutorCadastro(req.POST)
        user_form = AccountForm(req.POST)
        print(req.POST['username'])
        print(req.POST['email'])

        # Valida os formularios e verifica se o usuario ou email ja estao cadastrados
        if user_form.is_valid() and register_form.is_valid() and \
                register_form.is_valid_email(req.POST['email']) and \
                register_form.is_valid_username(req.POST['username']):

            u = user_form.save()
            u.set_password(u.password)
            u.save()

            a = register_form.save(commit=False)
            a.usuario = u
            a.save()

            return HttpResponseRedirect('/index/registrado/')

    cdict = load_menu_sidebar()
    cdict.update({'register_form': register_form, 'user_form': user_form})
    context = RequestContext(req, cdict)
    return render_to_response('cadastro.html', context)


def user_logout(req):
    logout(req)
    return HttpResponseRedirect('/')


def categoria(req, cat):
    cdict = load_menu_sidebar()
    categoria_select = Categoria.objects.get(nome=cat)
    receitas = Receita.objects.filter(categoria=categoria_select)
    cdict.update({'cat': cat, 'receitas': receitas})
    context = RequestContext(req, cdict)
    return render_to_response('receita_categoria.html', context)


def cadastro_receita(req):
    cdict = load_menu_sidebar()
    receita_cadastro = ReceitaCadastro()
    if req.method == 'POST':
        receita_cadastro = ReceitaCadastro(req.POST, req.FILES)
        if receita_cadastro.is_valid():
            receita = receita_cadastro.save()
            return HttpResponseRedirect('/detalhe_receita/{}/'.format(receita.pk))
    cdict.update({'receita_cadastro': receita_cadastro})
    context = RequestContext(req, cdict)
    return render_to_response('cadastro_receita.html', context)


def detalhe_receita(req, pk):
    cdict = load_menu_sidebar()

    receita = Receita.objects.get(pk=pk)
    comentario_form = ComentarForm()
    login_form = LoginForm()
    # Se for feito algum comentario
    if req.method == 'POST':
        if 'autenticado' in req.POST:
            comentario_form = ComentarForm(req.POST)
            if comentario_form.is_valid():
                comentario = comentario_form.save(commit=False)
                comentario.usuario = req.user
                comentario.receita = receita
                comentario.save()
        else:
            login_form = LoginForm(req.POST)
            if login_form.is_valid():
                do_login(req)

    # Database lookups
    ingredientes = Ingredientes.objects.filter(receita=receita)
    imagens = ReceitaImagem.objects.filter(ref=receita)
    # Busca apenas os 100 primeiros comentarios
    comentarios = Comentario.objects.filter(receita=receita)[:100]
    votos = Voto.objects.filter(receita=receita)
    voto_valor = [voto.valor for voto in votos]

    # Other variables
    ncomentarios = len(comentarios)
    nota = int(sum(voto_valor))/len(voto_valor) if len(voto_valor) > 0 else 5
    receita.instrucao = receita.instrucao.split('\n')
    receita.metodo_preparo = PREPARO_ESCOLHAS[receita.metodo_preparo][1]
    bebida = receita.categoria.nome == 'Bebidas'

    # Updating context
    cdict.update({'receita': receita, 'ingredientes': ingredientes, 'isbebida': bebida})
    cdict.update({'cat': receita.categoria.nome, 'imagens': imagens, 'nota': nota})
    cdict.update({'comentarios': comentarios, 'ncomentarios': ncomentarios})
    cdict.update({'comentario_form': comentario_form, 'login_form': login_form, 'id': pk})
    context = RequestContext(req, cdict)

    return render_to_response('receita.html', context)


def votacao(req):
    if req.method == 'POST':
        receita = Receita.objects.get(pk=req.POST['pk'])
        if not req.user.is_authenticated():
            return HttpResponse(
                json.dumps({'response': "Faca login para poder votar!"}),
                content_type="application/json"
            )
        allvotos = Voto.objects.filter(receita=receita, usuario=req.user).count()
        if allvotos > 0:
            return HttpResponse(
                json.dumps({'response': "Voce ja votou nessa receita!"}),
                content_type="application/json"
            )

        voto = Voto.objects.create(
            valor=req.POST['rating'],
            usuario=req.user,
            receita=receita
        )
        voto.save()
        return HttpResponse(
            json.dumps({'response': "Voto efetuado com sucesso!", 'type': "success"}),
            content_type="application/json"
        )
    return HttpResponse(
        json.dumps({'response': "Erro ao efetuar voto", 'type': "danger"}),
        content_type="application/json"
    )


def exportar_receita(req, pk):
    receita = Receita.objects.filter(pk=pk)


def receita_do_dia():
    pks = [1]
    return Receita.objects.filter(pk__in=pks)


def top_receitas():
    pks = [3,5,6]
    return Receita.objects.filter(pk__in=pks)


def load_menu_sidebar():
    return {
        'categorias' : Categoria.objects.all(),
        'receita_do_dia': receita_do_dia(),
        'top_receitas': top_receitas()
    }


def busca(req):
    receitas = Receita.objects.all()
    rec_nomes = [[x.nome, x.id] for x in receitas]
    response = {'receitas': rec_nomes}
    return HttpResponse(json.dumps(response), content_type="application/json")
