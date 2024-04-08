from django.db import models

# Create your models here.
class Tip(models.Model):
    codigo = models.CharField(primary_key=True,max_length=4)
    nombre = models.CharField(max_length=90)
    descripcion = models.CharField( max_length=2000 )
    publish = models.BooleanField(default=True)
    date = models.DateTimeField(auto_now_add=True) # Usa auto_now_add=True en lugar de auto_now=True
    imageproj = models.FileField(upload_to='tips/', null=True,)

    def __str__(self):
        texto = "[{0}] {1}"
        if self.publish:
            tp = "On"
        else:
            tp = "Off"    
        return texto.format(self.nombre,tp)