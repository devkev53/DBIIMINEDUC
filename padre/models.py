from django.db import models

from core.models import PersonaBase

# Create your models here.

class PadreFamilia(PersonaBase):

    class Meta:
        verbose_name = "PadreFamilia"
        verbose_name_plural = "PadreFamilias"
        db_table = 'PadreFamilia'

    def __str__(self):
        return '%s' % (self.nombre_completo())
