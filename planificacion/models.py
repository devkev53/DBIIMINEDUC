from django.db import models

# Importamos pra la conecxion a la BD
from django.db import connection

from django.core.exceptions import ValidationError

from comite.models import Comite, Fondo

# Create your models here.

class Planificacion(models.Model):
    comite = models.ForeignKey(Comite, on_delete=models.CASCADE, verbose_name='Comite')
    descripcion = models.TextField('Descripcion')
    fecha_crea = models.DateField("Fecha Creacion", auto_now_add=True)
    ciclo = models.PositiveSmallIntegerField('Ciclo')

    class Meta:
        ordering = ['-ciclo']
        unique_together = ['comite', 'ciclo']
        verbose_name = "Planificacion"
        verbose_name_plural = "Planificaciones"
        db_table = 'Planificacion'

    def actividades_registradas(self):
        valor = 0
        for a in Actividad.objects.all():
            if a.plainficacion == self.id:
                valor = valor+1
        return valor

    def actividades_finalizadas(self):
        valor = 0
        for a in Actividad.objects.all():
            if a.plainficacion == self.id:
                if a.estado == 0:
                    valor = valor+1
        return valor

    def actividades_aprobadas(self):
        valor = 0
        for a in Actividad.objects.all():
            if a.plainficacion == self.id:
                if a.estado == 1:
                    valor = valor+1
        return valor

    def llamar_saldo(self):
        saldo = Fondo.objects.filter(comite=self.comite, ciclo=self.ciclo).get()
        return saldo.saldo

    def __str__(self):
        return 'Ciclo: %s, %s' % (self.ciclo, self.comite)

ACTIVIDAD_CHOICES = [
    ('Deportiva', 'Deportiva'),
    ('Cultural', 'Cultural'),
    ('Social', 'Social'),
    ('Artistica', 'Artistica'),
    ('Academica', 'Academica'),
]

class Actividad(models.Model):
    tipo = models.CharField('Tipo de Actividad', choices=ACTIVIDAD_CHOICES, max_length=25)
    descripcion = models.TextField('Descripcion')
    fecha_prog = models.DateField('Fecha Programada')
    costo = models.DecimalField('Costo', max_digits=10, decimal_places=2)
    estado = models.PositiveSmallIntegerField('Estado', default=2)
    fecha_crea = models.DateField("Fecha Creacion", auto_now_add=True)
    plainficacion = models.ForeignKey(Planificacion, on_delete=models.CASCADE, verbose_name='Comite')

    class Meta:
        verbose_name = "Actividad"
        verbose_name_plural = "Actividads"
        db_table = 'Actividad'

    def costo_real(self):
        saldo = 0
        for pago in PagoActividad.objects.filter(actividad=self.id):
            saldo = pago.valor+saldo
        saldo = float(saldo)
        return saldo

    def estado_actividad(self):
        if self.estado == 0:
            return 'Finalizada'
        elif self.estado == 1:
            return 'Autorizada'
        elif self.estado == 2:
            return 'Ingresada'

    def __str__(self):
        return '%s %s' % (self.plainficacion.ciclo, self.descripcion)

def comite_directory_path(instance, filename):
    return 'Actividad/' + filename

class PagoActividad(models.Model):
    actividad = models.ForeignKey(Actividad, on_delete=models.CASCADE, verbose_name='Actividad')
    factura = models.FileField(upload_to='uploads/', blank=True)
    valor = models.DecimalField('Costo', max_digits=10, decimal_places=2)
    descripcion = models.TextField('Descripcion')
    fecha_crea = models.DateField("Fecha Creacion", auto_now_add=True)

    class Meta:
        db_table = 'PagoActividad'
        verbose_name = "PagoActividad"
        verbose_name_plural = "PagoActividades"

    def validar_retiro_sql(self):
        ciclo = self.actividad.plainficacion.ciclo
        comite = self.actividad.plainficacion.comite
        fondo = Fondo.objects.filter(comite=comite, ciclo=ciclo).get()
        saldo = fondo.saldo
        dato = 0
        result = False
        with connection.cursor() as cursor:
            dato = cursor.callfunc("VALIDAR_PAGO_ACTIVIDAD", int, [saldo, self.valor, fondo.pk])
        # Segun el procedimiento creado si retorna 0 es que existe uno o mas comites
        if  dato == 1:
            result = True
        else:
            result = False
        return result

    def __str__(self):
        return 'Costo: %s, fecha_crea: %s' % (
            self.valor, self.fecha_crea
            )

    def clean(self, **kwargs):
        super(PagoActividad, self).clean()
        # Si nos retorna verdadero lanzamos un error
        respuestaSQL_Retiro = self.validar_retiro_sql()
        if respuestaSQL_Retiro is True:
            raise ValidationError('No se Cuenta con Suficiente Saldo')