from django import forms
from django.db.models import F, Q
from .models import RegistroParqueo, Vehiculo, Zona, Pago,Empleado,  Cliente, Ingreso, Factura, Promocion,Persona,Propietario

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = '__all__'


class PersonaForm(forms.ModelForm):
    class Meta:
        model = Persona
        fields = '__all__'
        widgets = {
            'nombres': forms.TextInput(attrs={'class': 'form-control'}),
            'apellidos': forms.TextInput(attrs={'class': 'form-control'}),
            'tipo_documento': forms.TextInput(attrs={'class': 'form-control'}),
            'numero_documento': forms.TextInput(attrs={'class': 'form-control'}),
            'correo': forms.EmailInput(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
        }

class PropietarioForm(forms.ModelForm):
    class Meta:
        model = Propietario
        fields = '__all__'


class IngresoForm(forms.ModelForm):
    class Meta:
        model = Ingreso
        fields = '__all__'

class FacturaForm(forms.ModelForm):
    class Meta:
        model = Factura
        fields = '__all__'

class PromocionForm(forms.ModelForm):
    class Meta:
        model = Promocion
        fields = '__all__'

class EmpleadoForm(forms.ModelForm):
    class Meta:
        model = Empleado
        fields = '__all__'

class ZonaForm(forms.ModelForm):
    class Meta:
        model = Zona
        fields = '__all__'
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'capacidad': forms.NumberInput(attrs={'class': 'form-control'}),
        }

class VehiculoForm(forms.ModelForm):
    class Meta:
        model = Vehiculo
        fields = [
            'placa', 'tipo', 'zona_asignada', 'marca',
            'modelo', 'color', 'cliente', 'observaciones'
        ]

class RegistroEntradaForm(forms.ModelForm):
    class Meta:
        model = RegistroParqueo
        fields = ['vehiculo', 'zona', 'notas']  # Asegúrate que estos campos existan
        widgets = {
            'vehiculo': forms.Select(attrs={
                'class': 'form-control',
                'required': 'true',
                'pattern': r'[A-Za-z]{3}-?\d{3,4}',
                'title': 'Formato: ABC-123 o ABC123'
            }),
            'zona': forms.Select(attrs={
                'class': 'form-control',
                'required': 'true'
            }),
            'notas': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Observaciones...'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'vehiculo' in self.fields:
            self.fields['vehiculo'].queryset = Vehiculo.objects.all()
        if 'zona' in self.fields:
            self.fields['zona'].queryset = Zona.objects.filter(ocupados__lt=F('capacidad'))

class PagoForm(forms.ModelForm):
    class Meta:
        model = Pago
        fields = ['registro_parqueo', 'monto', 'metodo_pago', 'comprobante', 'referencia_pago']
        widgets = {
            'registro_parqueo': forms.Select(attrs={
                'class': 'form-control select2',
                'required': True
            }),
            'monto': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0.01'
            }),
            'metodo_pago': forms.Select(attrs={
                'class': 'form-control',
                'required': True
            }),
            'comprobante': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: TRANS-12345'
            }),
            'referencia_pago': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: BANCO-789012'
            }),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        # Filtra registros pendientes de pago
        self.fields['registro_parqueo'].queryset = RegistroParqueo.objects.filter(
            estado='pendiente_pago'
        )
        
        # Si es edición, hacer algunos campos readonly
        if self.instance and self.instance.pk:
            self.fields['registro_parqueo'].disabled = True
            self.fields['monto'].disabled = True
            
        # Asignar empleado automáticamente si está disponible
        if user and hasattr(user, 'empleado'):
            self.instance.empleado = user.empleado

    def clean_monto(self):
        monto = self.cleaned_data.get('monto')
        if monto and monto <= 0:
            raise forms.ValidationError("El monto debe ser mayor que cero")
        return monto

class VehiculoForm(forms.ModelForm):
    class Meta:
        model = Vehiculo
        fields = ['placa', 'tipo', 'marca', 'modelo', 'color']
        widgets = {
            'placa': forms.TextInput(attrs={
                'class': 'form-control',
                'pattern': r'[A-Za-z]{3}-?\d{3,4}',
                'title': 'Formato: ABC-123 o ABC123'
            }),
        }