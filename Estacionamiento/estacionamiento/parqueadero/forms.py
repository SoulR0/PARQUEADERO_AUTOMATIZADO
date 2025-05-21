from django import forms
from .models import Vehiculo, RegistroParqueo

class VehiculoForm(forms.ModelForm):
    class Meta:
        model = Vehiculo
        fields = ['placa', 'tipo']  # sin 'propietario'


class RegistroEntradaForm(forms.ModelForm):
    class Meta:
        model = RegistroParqueo
        fields = ['vehiculo']  # Solo se selecciona el vehículo para la entrada
