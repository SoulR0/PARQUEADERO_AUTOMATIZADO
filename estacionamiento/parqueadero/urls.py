# parqueadero/urls.py

from django.urls import path
from . import views

urlpatterns = [
    # Ruta de prueba que puedes eliminar o editar después
    path('', views.home, name='home'),
    path('registrar-entrada/', views.registrar_entrada, name='registrar_entrada'),
]
