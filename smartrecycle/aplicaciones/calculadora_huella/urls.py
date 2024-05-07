from django.urls import path
from . import views

urlpatterns = [
    path('cuestionario/', views.cuestionario, name='cuestionario_inicio'),
    path('resultados/', views.resultados, name='resultados'),
    path('cuestionario/<int:pregunta_id>/', views.cuestionario, name='cuestionario'),
    path('historial/', views.historial, name='historial'),
    path('borrar_intentos/', views.borrar_intentos, name='borrar_intentos'),
]