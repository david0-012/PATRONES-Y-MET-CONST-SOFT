from django import forms
from .models import Reporte

class ReporteForm(forms.ModelForm):
    class Meta:
        model = Reporte
        # fields = '__all__'           Incluye todos los campos del modelo
        fields = ['nombre', 'email', 'consulta', 'mensaje']
