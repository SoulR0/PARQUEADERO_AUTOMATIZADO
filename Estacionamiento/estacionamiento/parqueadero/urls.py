from django.urls import path
from . import views

urlpatterns = [
    path('', views.mi_vista, name='inicio'),
    path('vehiculos/', views.lista_vehiculos, name='lista_vehiculos'),
]