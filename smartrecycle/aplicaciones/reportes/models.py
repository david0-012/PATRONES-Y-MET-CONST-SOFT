from django.db import models

opciones_consulta = [
    [0, "Consulta"],
    [1, "Reclamo"],
    [2, "Sugerencia"],
    [3, "Error"],
    [4, "Otro"],
]

# Create your models here.
class Reporte(models.Model):
    nombre = models.CharField(max_length=50)
    email = models.EmailField()
    consulta = models.IntegerField(choices=opciones_consulta)
    mensaje = models.TextField()
    complete = models.BooleanField(default=False)

    def __str__(self):
        return self.nombre