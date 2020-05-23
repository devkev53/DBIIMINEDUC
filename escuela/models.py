from django.db import models
from django.db import connection

# Importamos la libreria para random
import random

from core.models import Departamento, Municipio

# Create your models here.

# Creacion de un
def get_rand_string():
    """Devuelve un string de 10 caracteres aleatorios"""
    return ''.join(random.choice(
            'abcdefghijklmnopqrstuvwxyz') for i in
            range(3)) + ''.join(random.choice(
            '0123456789') for i in
            range(3))

class Escuela(models.Model):
    codigo = models.CharField('Codigo', primary_key=True, unique=True, max_length=10, default=get_rand_string)
    nombre = models.CharField('Nombre', max_length=200)
    direccion = models.CharField('Direccion', max_length=200)
    departamento = models.ForeignKey(Departamento, on_delete=models.CASCADE, verbose_name='Departamento')
    municipio = models.ForeignKey(Municipio, on_delete=models.CASCADE, verbose_name='Municipio')
    fecha_crea = models.DateField('Fecha', auto_now_add=True)

    class Meta:
        verbose_name = "Escuela"
        verbose_name_plural = "Escuelas"
        db_table = 'Escuela'

    # Llamamos a una funcion en la base de datos, y evaluamos si existe un Usuario
    def existe_usuario_sql(self):
        dato = 0
        result = False
        with connection.cursor() as cursor:
            dato = cursor.callfunc("FN_GET_USUARIO", int, [self.codigo])
        # Segun el procedimiento creado si retorna 0 es que existe uno o mas comites
        if  dato == 0:
            result = True
        else:
            result = False
        return result

    # Llamamos a una funcion en la base de datos, y evaluamos si existe un comite
    def existe_fondo_sql(self):
        dato = 0
        result = False
        with connection.cursor() as cursor:
            dato = cursor.callfunc("FN_GET_FONDO", int, [self.codigo])
        # Segun el procedimiento creado si retorna 0 es que existe uno o mas comites
        if  dato == 0:
            result = True
        else:
            result = False
        return result


    def asignar_numeracion(self):
        new_id = ''
        new_id = (str(self.municipio.codigo)+self.codigo.upper())
        for escuela in Escuela.objects.all():
            if escuela.codigo == self.codigo:
                self.codigo= escuela.codigo
            else:
                self.codigo = new_id

    def __str__(self):
        return '%s' % (self.nombre)

    def clean(self, **kwargs):
        super(Escuela, self).clean()
        self.nombre = self.nombre.upper()
        self.direccion = self.direccion.upper()
        n1 = self.municipio.codigo
        n2 = self.codigo
        if len(n2)>6:
            n3 = n2[4:]
            self.codigo = (str(n1)+str(n3)).upper()
        else:
            self.codigo = (str(n1)+str(n2)).upper()

    '''
    def save(self, *args, **kwargs):
        self.asignar_numeracion()
        super(Escuela, self).save(*args, **kwargs)
    '''


class Comite(models.Model):
    nombre = models.CharField('Nombre', max_length=200)
    descripcion = models.TextField('Descripcion')
    fecha_crea = models.DateField("Fecha Creacion", auto_now_add=True)
    escuela = models.OneToOneField(Escuela, on_delete=models.CASCADE, verbose_name='Escuela')

    class Meta:
        verbose_name = "Comite"
        verbose_name_plural = "Comites"
        db_table = 'Comite'

    def saldo(self):
        from comite.models import Fondo
        fondo = Fondo.objects.filter(comite=self.pk).get()
        return '%s' % (fondo.saldo)

    def __str__(self):
        return '%s' % (self.nombre)

    def clean(self, **kwargs):
        super(Comite, self).clean()
        self.nombre = self.nombre.upper()
        self.descripcion = self.descripcion.upper()