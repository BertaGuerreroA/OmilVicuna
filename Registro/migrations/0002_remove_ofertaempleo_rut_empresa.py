# Generated by Django 4.2.15 on 2024-09-14 19:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Registro', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ofertaempleo',
            name='rut_empresa',
        ),
    ]
