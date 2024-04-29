from django.http import HttpResponse
from django.template import loader
from .forms import ReporteForm
from django.shortcuts import render

def reporte(request):
  data = {
    'form': ReporteForm() # Instancia del formulario ReporteForm
  }

  if request.method == 'POST':

    formulario = ReporteForm(data = request.POST)

    if formulario.is_valid():

      formulario.save()
      data['mensaje'] = "Reporte enviado con exito"

    else:
      data['form'] = formulario
      data['mensaje'] = "Error al enviar reporte"

  return render(request, 'reporte.html', data) # Renderiza el template reporte.html con el formulario ReporteForm como parametro