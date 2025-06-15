# usuarios/urls.py (ejemplo básico)
from django.urls import path
from . import views

app_name = 'usuarios'

urlpatterns = [
    path('crear/', views.crear_usuario, name='crear'),
]