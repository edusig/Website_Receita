from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.sitemaps.views import sitemap
from receita.sitemap import ReceitaSitemap, StaticSitemap, CategoriaSitemap

admin.autodiscover()

sitemaps = {
    'static': StaticSitemap(),
    'categoria': CategoriaSitemap(),
    'receita': ReceitaSitemap(),
}

urlpatterns = patterns(
    '',
    url(r'^$', 'receita.views.index', name='index'),
    url(r'^index/([a-zA-Z0-9 -_]+)/$', 'receita.views.index_not', name='index_not'),
    url(r'^login/$', 'receita.views.userlogin', name='login'),
    url(r'^logout/$', 'receita.views.user_logout', name='logout'),
    url(r'^register/', 'receita.views.register', name='cadastro'),
    url(r'^categoria/(?P<cat>[a-zA-Z0-9 -_]+)/', 'receita.views.categoria', name='categoria'),
    url(r'^cadastro_receita/', 'receita.views.cadastro_receita', name='cadastro_receita'),
    url(r'^detalhe_receita/([a-zA-Z0-9 -_]+)/', 'receita.views.detalhe_receita', name='detalhe_receita'),
    url(r'^busca/', 'receita.views.busca', name='busca'),
    url(r'^exportar_receita/([a-zA-Z0-9 -_]+)/', 'receita.views.exportar_receita', name='exportar_receita'),
    url(r'^votar/', 'receita.views.votacao', name='votacao'),
    url(r'^robots\.txt$', 'receita.views.robots', name='robots'),
    url(r'^sitemap\.xml$', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    url(r'^admin/', include(admin.site.urls)),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
