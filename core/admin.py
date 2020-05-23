from django.contrib import admin
from .models import Departamento, Municipio

# Register your models here.

class DepartamentoAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'nombre')

class MunicipioAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'nombre', 'departamento')
    list_filter = ('departamento',)

admin.site.register(Departamento, DepartamentoAdmin)
admin.site.register(Municipio, MunicipioAdmin)



'''
class Municipio(models.Model):
	codigo = models.PositiveSmallIntegerField(primary_key=True, unique=True)
	nombre = models.CharField(max_length=100)
	departamento = models.ForeignKey(Departamento, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Municipio"
        verbose_name_plural = "Municipios"
        db_table = 'Municipio'

    def asignar_id_departamento():
    	id_depto = 0
    	new_codigo = 0
    	# Obtenemos el Departamento que Seleccionamos lo pasamos a string
    	id_depto = str(self.departamento.codigo)
    	# Obtenemos el codigo ingresado y lo concatenamos al del depto
    	new_codigo = (str(self.codigo)+id_depto)
    	# Volvemos a pasar a int el codigo
    	new_codigo int(new_codigo)
    	# Lo guardamos como el codigo
    	self.codigo = new_codigo

    def __str__(self):
        return '%s' % (self.nombre)

    def save(self, *args, **kwargs):
    	asignar_id_departamento()
        super(Municipio, self).save(*args, **kwargs)
'''