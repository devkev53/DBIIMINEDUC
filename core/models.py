from django.db import models
from django.core.exceptions import ValidationError
# Create your models here.


class Departamento(models.Model):
    codigo = models.CharField('Codigo', primary_key=True, unique=True, max_length=2)
    nombre = models.CharField('Nombre', max_length=100, blank=True)

    class Meta:
        verbose_name = "Departamento"
        verbose_name_plural = "Departamentos"
        db_table = 'Departamento'
        ordering = ['codigo',]

    def asignar_codigo(self):
        new_codigo = str(self.codigo)
        # Verificamos que el codigo sea de un digito para agregar el 0
        if len(self.codigo) < 2:
            new_codigo = ('0' + str(self.codigo))
        self.codigo = new_codigo

    def __str__(self):
        return '%s' %  (self.nombre)

    def save(self, *args, **kwargs):
        self.asignar_codigo()
        super(Departamento, self).save(*args, **kwargs)

class Municipio(models.Model):
    codigo = models.CharField('Codigo', primary_key=True, unique=True, max_length=4)
    nombre = models.CharField(max_length=100)
    departamento = models.ForeignKey(Departamento, on_delete=models.CASCADE, verbose_name='Departamento')

    class Meta:
        verbose_name = "Municipio"
        verbose_name_plural = "Municipios"
        db_table = 'Municipio'
        ordering = ['codigo',]

    def asignar_id_departamento(self):
        id_depto = '0'
        new_codigo = self.codigo
        id_depto = str(self.departamento.codigo)
        # Verificamos que el codigo sea de un digito para agregar el 0
        if len(self.codigo) < 2:
            new_codigo = ('0' + new_codigo)
            print('El caracter tiene menos de dos letras')
        # Obtenemos el codigo ingresado y lo concatenamos al del depto
        new_codigo = str(id_depto + new_codigo)
        # Lo guardamos como el codigo
        self.codigo = new_codigo

    def __str__(self):
        return '%s' % (self.nombre)

    def clean(self, **kwargs):
        super(Municipio, self).clean()
        if len(self.codigo) < 3:
            pass
        else:
            raise ValidationError('Ingrese un codigo valido')

    def save(self, *args, **kwargs):
        self.asignar_id_departamento()
        super(Municipio, self).save(*args, **kwargs)

class PersonaBase(models.Model):
    dpi = models.CharField('DPI', max_length=15, primary_key=True, unique=True)
    nombres = models.CharField('Nombres', max_length=200)
    apellidos = models.CharField('Apellidos', max_length=200)
    fecha_nac = models.DateField('Fecha de Nacimiento', blank=True, null=True)
    direccion = models.CharField('Dirección', max_length=200, blank=True, null=True)

    class Meta:
        verbose_name = "PersonaBase"
        verbose_name_plural = "PersonaBases"
        abstract = True

    def nombre_completo(self):
        return '%s %s' % (self.nombres, self.apellidos)

    def __str__(self):
        return nombre_completo()
