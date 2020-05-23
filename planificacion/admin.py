from django.contrib import admin

from .models import Planificacion, Actividad, PagoActividad

# Register your models here.

admin.site.register(Planificacion)
admin.site.register(Actividad)
admin.site.register(PagoActividad)