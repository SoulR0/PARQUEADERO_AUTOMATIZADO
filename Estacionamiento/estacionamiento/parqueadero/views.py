from django.http import HttpResponse
from django.shortcuts import render

def mi_vista(request):
    return HttpResponse("¡Bienvenido al sistema de parqueadero!")

from django.shortcuts import render
from .models import Vehiculo

def lista_vehiculos(request):
    vehiculos = Vehiculo.objects.all()
    return render(request, 'vehiculos/lista_vehiculos.html', {'vehiculos': vehiculos})


