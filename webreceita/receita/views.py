from django.shortcuts import render_to_response
from django.template import RequestContext
from receita.models import *

# Create your views here.
def index(req):
    categorias = Categoria.objects.all()[:3]
    context = RequestContext(req, {'categorias':categorias})
    return render_to_response('index.html', context)