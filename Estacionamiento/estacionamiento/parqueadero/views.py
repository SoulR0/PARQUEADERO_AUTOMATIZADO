from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from django.db.models import Sum, F, Q
from django.utils import timezone
from decimal import Decimal
from .models import Vehiculo, RegistroParqueo, Zona, Pago, Tarifa
from .forms import (
    RegistroEntradaForm, VehiculoForm, PagoForm, ZonaForm, EmpleadoForm, ClienteForm, IngresoForm, FacturaForm, PromocionForm,PropietarioForm
)

from django.shortcuts import render
from .forms import PersonaForm  # asegúrate de tener este form

def crear_persona(request):
    if request.method == 'POST':
        form = PersonaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_personas')  # asegúrate de tener esa vista/url
    else:
        form = PersonaForm()
    return render(request, 'parqueadero/crear_persona.html', {'form': form})

def crear_empleado(request):
    form = EmpleadoForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('/')
    return render(request, 'empleados/crear_empleado.html', {'form': form})

def crear_cliente(request):
    form = ClienteForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('/')
    return render(request, 'clientes/crear_cliente.html', {'form': form})

def crear_ingreso(request):
    form = IngresoForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('/')
    return render(request, 'ingresos/crear_ingreso.html', {'form': form})

def crear_factura(request):
    form = FacturaForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('/')
    return render(request, 'facturas/crear_factura.html', {'form': form})

def crear_promocion(request):
    form = PromocionForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('/')
    return render(request, 'promociones/crear_promocion.html', {'form': form})

def crear_vehiculo(request):
    if request.method == 'POST':
        form = VehiculoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('inicio')  # O adonde quieras redirigir
    else:
        form = VehiculoForm()
    return render(request, 'vehiculos/crear_vehiculo.html', {'form': form})


def crear_zona(request):
    if request.method == 'POST':
        form = ZonaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_zonas')  # o la vista que prefieras
    else:
        form = ZonaForm()
    return render(request, 'zona/crear_zona.html', {'form': form})

def lista_registros_parqueo(request):
    registros = RegistroParqueo.objects.all().values()  # convierte a diccionario
    return JsonResponse(list(registros), safe=False)

def mi_vista(request):
    """Vista de inicio simple (puede servir como página de bienvenida)"""
    mensaje = """
    ¡Bienvenido al sistema de parqueadero!<br>
    Estacionamiento exclusivo para clientes autorizados.<br>
    Zona de estacionamiento vigilada. No nos hacemos responsables por objetos personales.<br>
    Respetar los espacios señalados. Gracias por su cooperación.
    """
    return HttpResponse(mensaje)

def lista_vehiculos(request):
    """Listado de todos los vehículos registrados"""
    vehiculos = Vehiculo.objects.all().select_related('cliente', 'zona_asignada')
    return render(request, 'parqueadero/vehiculos/lista.html', {'vehiculos': vehiculos})

from django.utils import timezone
from decimal import Decimal
from django.db.models import Sum, F
from django.shortcuts import render
from django.http import JsonResponse, Http404
from .models import RegistroParqueo, Zona, Pago

def dashboard(request):
    """Vista principal del panel de control"""
    registros_activos = RegistroParqueo.objects.filter(
        estado='activo'
    ).select_related('vehiculo', 'zona', 'empleado_entrada')
    
    zonas = Zona.objects.annotate(
        disponibles=F('capacidad') - F('ocupados')
    )
    
    # Estadísticas
    ocupacion_total = sum(zona.ocupados for zona in zonas)
    capacidad_total = sum(zona.capacidad for zona in zonas)

    # ✅ Cambio realizado aquí
    ingresos_hoy = Pago.objects.filter(
        fecha_pago__date=timezone.now().date()
    ).aggregate(total=Sum('monto'))['total'] or Decimal('0.00')
    
    context = {
        'registros_activos': registros_activos,
        'zonas': zonas,
        'ocupacion_total': ocupacion_total,
        'capacidad_total': capacidad_total,
        'ingresos_hoy': ingresos_hoy,
        'porcentaje_ocupacion': (ocupacion_total / capacidad_total * 100) if capacidad_total > 0 else 0,
    }
    return render(request, 'parqueadero/dashboard.html', context)




def agregar_vehiculo(request):
    if request.method == 'POST':
        form = VehiculoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Vehículo agregado exitosamente.')
            return redirect('lista_vehiculos')  # Asegúrate de tener esta vista y ruta
    else:
        form = VehiculoForm()

    return render(request, 'parqueadero/vehiculos/agregar.html', {'form': form})


def registro_entrada(request):
    """
    Vista para registrar la entrada de vehículos al parqueadero.
    Maneja tanto la visualización del formulario como el procesamiento de los datos.
    
    Args:
        request: HttpRequest object
    
    Returns:
        HttpResponse con el formulario o redirección al dashboard
    """
    if not request.user.is_authenticated or not hasattr(request.user, 'empleado'):
        messages.error(request, 'Acceso restringido: solo empleados autorizados')
        return redirect('inicio')
    
    if request.method == 'POST':
        form = RegistroEntradaForm(request.POST, user=request.user)
        if form.is_valid():
            try:
                registro = form.save(commit=False)
                registro.empleado_entrada = request.user.empleado
                registro.estado = 'activo'
                registro.save()
                
                # Actualizar contador de zona
                if registro.zona:
                    Zona.objects.filter(id=registro.zona.id).update(
                        ocupados=F('ocupados') + 1
                    )
                
                messages.success(
                    request,
                    f'Entrada registrada: {registro.vehiculo.placa} en Zona {registro.zona.nombre if registro.zona else "No asignada"}'
                )
                return redirect('dashboard')
            
            except Exception as e:
                messages.error(
                    request,
                    f'Error al registrar: {str(e)}'
                )
                # Log the error for debugging
                import logging
                logger = logging.getLogger(__name__)
                logger.error(f"Error en registro_entrada: {str(e)}")
    
    else:
        form = RegistroEntradaForm(user=request.user)
    
    # Obtener zonas con capacidad y datos adicionales
    zonas_disponibles = Zona.objects.filter(
        ocupados__lt=F('capacidad')
    ).annotate(
        disponibles=F('capacidad') - F('ocupados')
    ).values(
        'id', 'nombre', 'ocupados', 'capacidad', 'disponibles'
    )
    
    context = {
        'form': form,
        'zonas_disponibles': zonas_disponibles,
        'current_time': timezone.now().strftime("%Y-%m-%d %H:%M"),
    }
    
    return render(request, 'parqueadero/registro/entrada.html', context)

def registrar_salida(request, registro_id):
    """Registro de salida de vehículos"""
    registro = get_object_or_404(RegistroParqueo, id=registro_id, estado='activo')
    
    if request.method == 'POST':
        registro.hora_salida = timezone.now()
        registro.empleado_salida = request.user.empleado
        registro.estado = 'pendiente_pago'
        registro.calcular_cobro()
        registro.save()
        
        # Liberar espacio en la zona
        if registro.zona:
            registro.zona.ocupados = F('ocupados') - 1
            registro.zona.save()
        
        messages.success(request, 'Salida registrada correctamente')
        return redirect('dashboard')
    
    return render(request, 'parqueadero/registro/salida.html', {
        'registro': registro,
        'tiempo_estacionado': registro.tiempo_transcurrido
    })

def gestion_pagos(request):
    """Gestión de pagos pendientes"""
    pagos_pendientes = RegistroParqueo.objects.filter(
        estado='pendiente_pago'
    ).select_related('vehiculo')
    
    pagos_realizados = Pago.objects.order_by('-fecha')[:20]
    
    return render(request, 'parqueadero/pagos/gestion.html', {
        'pagos_pendientes': pagos_pendientes,
        'pagos_realizados': pagos_realizados
    })

def crear_pago(request, registro_id):
    """Procesamiento de pagos"""
    registro = get_object_or_404(RegistroParqueo, id=registro_id, estado='pendiente_pago')
    
    if request.method == 'POST':
        form = PagoForm(request.POST)
        if form.is_valid():
            pago = form.save(commit=False)
            pago.registro = registro
            pago.empleado = request.user.empleado
            pago.save()
            
            # Actualizar estado del registro
            registro.estado = 'finalizado'
            registro.save()
            
            messages.success(request, 'Pago registrado correctamente')
            return redirect('gestion_pagos')
    else:
        form = PagoForm(initial={
            'monto': registro.cobro,
            'metodo': 'efectivo'
        })
    
    return render(request, 'parqueadero/pagos/crear.html', {
        'form': form,
        'registro': registro
    })

#correccion en esta parte yair quintana
def detalle_zona(request, zona_id):
    try:
        zona = Zona.objects.get(pk=zona_id)
    except Zona.DoesNotExist:
        raise Http404("Zona no encontrada")

    data = {
        'id': zona.id,
        'nombre': zona.nombre,
        'capacidad': zona.capacidad,
    }
    return JsonResponse(data)

# API Views (opcional)
def api_zonas_disponibles(request):
    """Endpoint API para zonas disponibles"""
    zonas = Zona.objects.filter(
        ocupados__lt=F('capacidad')
    ).values('id', 'nombre', 'ocupados', 'capacidad')
    
    return JsonResponse(list(zonas), safe=False)

def api_registros_activos(request):
    """Endpoint API para registros activos"""
    registros = RegistroParqueo.objects.filter(
        estado='activo'
    ).select_related('vehiculo', 'zona').values(
        'id',
        'vehiculo__placa',
        'vehiculo__tipo',
        'zona__nombre',
        'hora_entrada'
    )
    
    return JsonResponse(list(registros), safe=False)

def lista_zonas(request):
    zonas = Zona.objects.all()
    data = [
        {
            'id': zona.id,
            'nombre': zona.nombre,
            'capacidad': zona.capacidad,
        }
        for zona in zonas
    ]
    return JsonResponse(data, safe=False)

def historial_pagos(request):
    pagos = Pago.objects.all().order_by('-fecha_pago')
    data = [
        {
            'id': pago.id,
            'monto': pago.monto,
            'fecha_pago': pago.fecha_pago,
            'metodo_pago': pago.metodo_pago,
            'registro': pago.registro.id if pago.registro else None,
        }
        for pago in pagos
    ]
    return JsonResponse(data, safe=False)

def crear_propietario(request):
    if request.method == 'POST':
        form = PropietarioForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_propietarios')  # o donde desees redirigir
    else:
        form = PropietarioForm()
    return render(request, 'parqueadero/crear_propietario.html', {'form': form})

#correccion en esta parte yair quintana
def api_historial_registros(request):
    registros = RegistroParqueo.objects.all().order_by('-hora_entrada')

    data = [
        {
            'id': registro.id,
            'placa': registro.placa,
            'hora_entrada': registro.hora_entrada,
            'hora_salida': registro.hora_salida,
            'zona': registro.zona.nombre if registro.zona else None,
            'estado': registro.estado,
        }
        for registro in registros
    ]
    return JsonResponse(data, safe=False)