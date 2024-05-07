from django.db import models
from django.contrib.auth.models import User

class Pregunta(models.Model):
    texto = models.CharField(max_length=200)
    orden = models.IntegerField()

    def __str__(self):
        return f"{self.orden}. {self.texto}"

class Opcion(models.Model):
    texto = models.CharField(max_length=200)
    valor = models.IntegerField()
    consejo = models.TextField(blank=True)  # Nuevo campo
    pregunta = models.ForeignKey(Pregunta, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.pregunta.texto} - {self.texto}"

class Intento(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    fecha = models.DateTimeField(auto_now_add=True)
    puntaje = models.IntegerField(null=True)  # Permitir valores nulos

    def __str__(self):
        return f"Intento de {self.usuario.username} en {self.fecha}: {self.puntaje}"

class Respuesta(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    pregunta = models.ForeignKey(Pregunta, on_delete=models.CASCADE)
    opcion = models.ForeignKey(Opcion, on_delete=models.CASCADE)
    intento = models.ForeignKey(Intento, on_delete=models.CASCADE, null=True, blank=True)  # Nuevo campo

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.intento:
            self.intento.puntaje = Respuesta.objects.filter(intento=self.intento).aggregate(models.Sum('opcion__valor'))['opcion__valor__sum']
            self.intento.save()

    def __str__(self):
        return f"{self.usuario.username} - {self.pregunta.texto} - {self.opcion.texto}"