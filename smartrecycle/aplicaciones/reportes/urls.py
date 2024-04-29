from django.urls import path
from . import views

urlpatterns = [
    path('reporte/', views.reporte, name='reporte'),
]