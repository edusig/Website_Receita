import models
from django.contrib import admin

admin.site.register(models.PerfilUsuario)
admin.site.register(models.Categoria)
admin.site.register(models.ReceitaImagem)
admin.site.register(models.Ingredientes)
admin.site.register(models.Comentario)
admin.site.register(models.Voto)
# admin.site.register(models.User)


class ReceitaGaleria(admin.StackedInline):
    model = models.ReceitaImagem
    extra = 1


class ReceitaIngredientes(admin.StackedInline):
    model = models.Ingredientes
    extra = 1


class ReceitaAdmin(admin.ModelAdmin):
    inlines = [ReceitaGaleria, ReceitaIngredientes]

admin.site.register(models.Receita, ReceitaAdmin)
