# Generated by Django 2.2 on 2020-05-19 06:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('escuela', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UsuarioEscuela',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('escuela', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='escuela.Escuela', verbose_name='Escuela')),
                ('usuario', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Usuario')),
            ],
            options={
                'verbose_name': 'UsuarioEscuela',
                'verbose_name_plural': 'UsuarioEscuelas',
            },
        ),
        migrations.CreateModel(
            name='UsuarioComite',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comite', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='escuela.Comite', verbose_name='Comite')),
                ('usuario', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Usuario')),
            ],
            options={
                'verbose_name': 'UsuarioComite',
                'verbose_name_plural': 'UsuarioComites',
            },
        ),
    ]