from django import forms
from .models import Vehiculo, Espacio

class VehiculoForm(forms.ModelForm):
    class Meta:
        model = Vehiculo
        fields = [
            'placa',
            'tipo',
            'zona_asignada',
            'espacio',
            'marca',
            'modelo',
            'color',
            'cliente',
            'observaciones',
        ]
        widgets = {
            'observaciones': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super(VehiculoForm, self).__init__(*args, **kwargs)
        # Solo mostrar espacios disponibles
        self.fields['espacio'].queryset = Espacio.objects.filter(ocupado=False)
