# Generated by Django 5.0.3 on 2024-05-06 18:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reportes', '0002_reporte_complete'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reporte',
            name='consulta',
            field=models.IntegerField(choices=[(0, 'Consulta'), (1, 'Reclamo'), (2, 'Sugerencia'), (3, 'Error'), (4, 'Otro')]),
        ),
    ]
