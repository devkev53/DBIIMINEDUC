from django.contrib import admin

from .models import Fondo, MovimientoFondo, Integrante

# Register your models here.

class FondoAdmin(admin.ModelAdmin):
    list_display = ('ciclo', 'comite', 'fecha', 'montoInicial', 'estado', 'saldo')

admin.site.register(Integrante)
admin.site.register(Fondo, FondoAdmin)
admin.site.register(MovimientoFondo)