from django.http import HttpResponse
from django.shortcuts import render

def mi_vista(request):
    mensaje = """
    ¡Bienvenido al sistema de parqueadero!<br>
    Estacionamiento exclusivo para clientes autorizados.<br>
    Zona de estacionamiento vigilada. No nos hacemos responsables por objetos personales.<br>
    Respetar los espacios señalados. Gracias por su cooperación.
    """
    return HttpResponse(mensaje)

from django.shortcuts import render
from .models import Vehiculo

def lista_vehiculos(request):
    vehiculos = Vehiculo.objects.all()
    return render(request, 'vehiculos/lista_vehiculos.html', {'vehiculos': vehiculos})

