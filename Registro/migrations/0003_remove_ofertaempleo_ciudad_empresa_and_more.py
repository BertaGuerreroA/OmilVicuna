# Generated by Django 4.2.15 on 2024-09-14 19:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Registro', '0002_remove_ofertaempleo_rut_empresa'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ofertaempleo',
            name='ciudad_empresa',
        ),
        migrations.RemoveField(
            model_name='ofertaempleo',
            name='email_empresa',
        ),
        migrations.RemoveField(
            model_name='ofertaempleo',
            name='fecha_incorporacion_trabajo',
        ),
        migrations.RemoveField(
            model_name='ofertaempleo',
            name='giro_empresa',
        ),
        migrations.RemoveField(
            model_name='ofertaempleo',
            name='telefono_empresa',
        ),
    ]
