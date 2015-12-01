from django.contrib.sitemaps import Sitemap
from models import Receita, Categoria


class ReceitaSitemap(Sitemap):
    changefreq = "monthly"

    def items(self):
        return Receita.objects.all()


class StaticSitemap(Sitemap):

    def items(self):
        return ['index', 'login', 'cadastro']

    def location(self, obj):
        locations = {
            'index': '/',
            'login': '/login/',
            'cadastro': '/register/'
        }
        return locations[obj]


class CategoriaSitemap(Sitemap):
    changefreq = "daily"

    def items(self):
        return Categoria.objects.all()
