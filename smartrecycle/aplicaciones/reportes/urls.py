from django.urls import path
from . import views

urlpatterns = [
    path('reporteForm/', views.reporteForm, name='reporteForm'),
]