# Generated by Django 5.0.3 on 2024-05-05 23:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('calculadora_huella', '0005_respuesta_intento'),
    ]

    operations = [
        migrations.AlterField(
            model_name='intento',
            name='puntaje',
            field=models.IntegerField(null=True),
        ),
    ]
