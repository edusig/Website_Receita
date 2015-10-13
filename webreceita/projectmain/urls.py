from django.conf.urls import patterns, include, url
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns(
    #url(r'^webreceita/', include('webreceita.foo.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
