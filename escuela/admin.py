from django.contrib import admin
from .models import Escuela, Comite

# Register your models here.

class EscuelaAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'nombre', 'direccion', 'departamento', 'municipio', 'existe_fondo_sql', 'existe_usuario_sql', 'fecha_crea')
    list_filter = ('departamento', 'municipio',)

class ComiteAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'descripcion', 'escuela', 'fecha_crea')
    list_filter = ('escuela__departamento', 'escuela',)

admin.site.register(Escuela, EscuelaAdmin)
admin.site.register(Comite, ComiteAdmin)