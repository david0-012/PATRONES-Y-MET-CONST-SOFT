from django.db import models

class Lugares(models.Model):
    name = models.CharField(max_length=250, verbose_name='Nombre Sucursal')
    address = models.CharField(max_length=250, verbose_name='Dirección')
    lat = models.FloatField(verbose_name='Latitud')
    lng = models.FloatField(verbose_name='Longitud')

    class Meta:
        verbose_name = 'Punto de Reciclaje'
        verbose_name_plural = 'Puntos de Reciclaje'
        ordering = ['name']

    def __str__(self):
        return self.name


