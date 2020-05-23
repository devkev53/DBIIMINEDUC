from django.db import models

from django.db.models.signals import post_delete
from django.dispatch import receiver

from django.contrib.auth.models import User
from django.contrib.auth.models import Group

from escuela.models import Escuela
from escuela.models import Comite
# Create your models here.

class PerfilUsuario(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Usuario')

    class Meta:
        verbose_name = "PerfilUsuario"
        verbose_name_plural = "PerfilUsuarios"
        abstract = True

    def __str__(self):
        return '%s' % (self.usuario)

class UsuarioEscuela(PerfilUsuario):
    escuela = models.OneToOneField(Escuela, on_delete=models.CASCADE, verbose_name='Escuela')

    class Meta:
        verbose_name = "UsuarioEscuela"
        verbose_name_plural = "UsuarioEscuelas"

    def __str__(self):
        return '%s' % (self.usuario)

    def save(self, *args, **kwargs):
        g = Group.objects.get(name='USUARIOESCUELA')
        g.user_set.add(self.usuario)
        super(UsuarioEscuela, self).save(*args, **kwargs)

class UsuarioComite(PerfilUsuario):
    comite = models.OneToOneField(Comite, on_delete=models.CASCADE, verbose_name='Comite')

    class Meta:
        verbose_name = "UsuarioComite"
        verbose_name_plural = "UsuarioComites"

    def __str__(self):
        return '%s' % (self.usuario)

    def save(self, *args, **kwargs):
        g = Group.objects.get(name='USUARIOCOMITE')
        g.user_set.add(self.usuario)
        super(UsuarioComite, self).save(*args, **kwargs)

# Borrar usuario al eiminar USUARIOESCUELA
@receiver(models.signals.post_delete, sender=UsuarioEscuela)
def delete_file(sender, instance, *args, **kwargs):
    """ Deletes image files on `post_delete` """
    user = User.objects.filter(id=instance.usuario.id).delete()

# Borrar usuario al eiminar USUARIOECOMITE
@receiver(models.signals.post_delete, sender=UsuarioComite)
def delete_file(sender, instance, *args, **kwargs):
    """ Deletes image files on `post_delete` """
    user = User.objects.filter(id=instance.usuario.id).delete()
