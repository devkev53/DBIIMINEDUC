from django.db import models

# Importamos pra la conecxion a la BD
from django.db import connection

from django.core.exceptions import ValidationError

from escuela.models import Escuela, Comite
from padre.models import PadreFamilia
import datetime

# Create your models here.

PUESTOS_CHOICES = [
    ('1', 'Presidente'),
    ('2', 'Vice Presidente'),
    ('3', 'Secretario'),
    ('4', 'Tesorero'),
    ('5', 'Vocal'),
]

class Integrante(models.Model):
    comite = models.ForeignKey(Comite, on_delete=models.CASCADE, verbose_name='Comite')
    puesto = models.CharField('Puesto', choices=PUESTOS_CHOICES, max_length=1)
    padre = models.OneToOneField(PadreFamilia, on_delete=models.CASCADE, verbose_name='Padre de Familia', blank=True)

    def retornarPuesto(self):
        if self.puesto == '1':
            return 'Presidente'
        elif self.puesto == '2':
            return 'Vice-Presidente'
        elif self.puesto == '3':
            return 'Secretario'
        elif self.puesto == '4':
            return 'Tesorero'
        else:
            return 'Vocal'


    class Meta:
        ordering = ['puesto']
        unique_together = ['puesto', 'comite']
        verbose_name = "Integrante"
        verbose_name_plural = "Integrantes"

    def __str__(self):
        return '%s %s: %s' % (self.pk, self.retornarPuesto(), self.padre)


class Fondo(models.Model):
    comite = models.ForeignKey(Comite, on_delete=models.CASCADE, verbose_name='Comite')
    fecha = models.DateField('Fecha de Creacion', auto_now_add=True)
    montoInicial = models.DecimalField('Monto Inicial', max_digits=10, decimal_places=2, default=0.00)
    estado = models.BooleanField('Estado')
    saldo = models.DecimalField('Saldo', max_digits=10, decimal_places=2)
    ciclo = models.PositiveSmallIntegerField('Ciclo')


    class Meta:
        unique_together = ['ciclo', 'comite']
        verbose_name = "Fondo"
        verbose_name_plural = "Fondos"
        db_table = 'Fondo'
        ordering = ['-ciclo']

    def estado(self):
        if self.estado is True:
            return 'Activo'
        else:
            return 'Inactivo'

    def __str__(self):
        return '%s %s' % (self.comite, self.ciclo)

class MovimientoFondo(models.Model):
    fondo = models.ForeignKey(Fondo, on_delete=models.CASCADE, verbose_name='Fondo')
    fecha = models.DateField('Fecha', auto_now_add=True)
    valor = models.DecimalField('Valor', max_digits=10, decimal_places=2)
    tipoMovimiento = models.BooleanField('Tipo de Movimiento')
    observaciones = models.TextField('Observaciones')
    ciclo = models.PositiveSmallIntegerField('Ciclo')


    class Meta:
        ordering = ['-tipoMovimiento']
        verbose_name = "MovimientoFondo"
        verbose_name_plural = "MovimientosFondo"
        db_table = 'MovimientosFondo'


    def tipo_movimiento(self):
        if self.tipoMovimiento is True:
            return 'Deposito'
        else:
            return 'Retiro'

    def __str__(self):
        return 'Comite: %s, Tipo: %s, Fecha: %s, Valor: %s' % (
            self.fondo.comite, self.tipo_movimiento(),
            self.fecha, self.valor
            )

    ''' Llamamos a una funcion en la base de datos,
        y evaluamos si existe un movimiento de deposito de este año '''
    def validar_deposito_sql(self):
        result = False
        year = datetime.date.today().year
        int(year)
        # Obtenemos todos los movimientos para este fondo
        # Segun el procedimiento creado si retorna 0 es que existe uno o mas comites
        if  MovimientoFondo.objects.filter(fondo=self.fondo, tipo=True, ciclo=year).exists():
            result = True
        else:
            result = False
        return result


    def clean(self, **kwargs):
        super(MovimientoFondo, self).clean()
        # Si nos retorna verdadero lanzamos un error
        respuestaSQL_Deposito = self.validar_deposito_sql()
        if respuestaSQL_Deposito is True:
            raise ValidationError('Ya existe una asignacion')