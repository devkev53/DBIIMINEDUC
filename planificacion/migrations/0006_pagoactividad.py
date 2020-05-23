# Generated by Django 2.2 on 2020-05-22 04:41

from django.db import migrations, models
import django.db.models.deletion
import planificacion.models


class Migration(migrations.Migration):

    dependencies = [
        ('planificacion', '0005_actividad_tipo'),
    ]

    operations = [
        migrations.CreateModel(
            name='PagoActividad',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('factura', models.FileField(upload_to=planificacion.models.comite_directory_path, verbose_name='Comprobante')),
                ('costo', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Costo')),
                ('descripcion', models.TextField(verbose_name='Descripcion')),
                ('fecha_crea', models.DateField(auto_now_add=True, verbose_name='Fecha Creacion')),
                ('actividad', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='planificacion.Actividad', verbose_name='Actividad')),
            ],
            options={
                'verbose_name': 'PagoActividad',
                'verbose_name_plural': 'PagoActividades',
                'db_table': 'PagoActividad',
            },
        ),
    ]
