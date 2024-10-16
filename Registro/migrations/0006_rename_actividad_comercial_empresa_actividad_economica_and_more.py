# Generated by Django 4.2.15 on 2024-09-14 20:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Registro', '0005_remove_empresa_tamaño_empresa_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='empresa',
            old_name='actividad_comercial',
            new_name='actividad_economica',
        ),
        migrations.AddField(
            model_name='empresa',
            name='descripcion',
            field=models.TextField(blank=True, null=True, verbose_name='Descripción de la Empresa'),
        ),
        migrations.AlterField(
            model_name='empresa',
            name='tamagno_empresa',
            field=models.CharField(blank=True, choices=[('MCR', 'Micro'), ('PE', 'Pequeña'), ('ME', 'Mediana'), ('GR', 'Grande')], max_length=3, null=True, verbose_name='Tamaño de Empresa'),
        ),
    ]
