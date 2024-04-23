from django.http import HttpResponse
from django.template import loader

def reporteForm(request):
  template = loader.get_template('formulario.html')
  return HttpResponse(template.render())