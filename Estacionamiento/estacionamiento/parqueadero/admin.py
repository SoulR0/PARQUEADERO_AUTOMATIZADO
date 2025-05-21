from django.contrib import admin
from .models import (
    Zona, Vehiculo, RegistroParqueo, Tarifa, 
    Cliente, Empleado, Incidente, Promocion, Pago, Factura
)

# Configuraciones personalizadas para cada modelo

@admin.register(Zona)
class ZonaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'ubicacion', 'capacidad', 'ocupados', 'espacios_disponibles', 'habilitada')
    list_filter = ('habilitada', 'nombre')
    search_fields = ('nombre', 'ubicacion')
    actions = ['habilitar_zonas', 'deshabilitar_zonas']

    def espacios_disponibles(self, obj):
        return obj.capacidad - obj.ocupados
    espacios_disponibles.short_description = 'Espacios Disponibles'

    def habilitar_zonas(self, request, queryset):
        queryset.update(habilitada=True)
    habilitar_zonas.short_description = "Habilitar zonas seleccionadas"

    def deshabilitar_zonas(self, request, queryset):
        queryset.update(habilitada=False)
    deshabilitar_zonas.short_description = "Deshabilitar zonas seleccionadas"

@admin.register(Vehiculo)
class VehiculoAdmin(admin.ModelAdmin):
    list_display = ('placa', 'tipo', 'marca', 'modelo', 'color', 'cliente', 'zona_asignada')
    list_filter = ('tipo', 'zona_asignada', 'marca')
    search_fields = ('placa', 'cliente__user__username', 'marca', 'modelo')
    autocomplete_fields = ('cliente', 'zona_asignada')
    readonly_fields = ('fecha_registro',)

    fieldsets = (
        ('Información Básica', {
            'fields': ('placa', 'tipo', 'zona_asignada')
        }),
        ('Detalles del Vehículo', {
            'fields': ('marca', 'modelo', 'color', 'cliente')
        }),
        ('Metadata', {
            'fields': ('observaciones',),
            'classes': ('collapse',)
        })
    )

@admin.register(RegistroParqueo)
class RegistroParqueoAdmin(admin.ModelAdmin):
    list_display = ('id', 'vehiculo', 'hora_entrada', 'hora_salida', 'estado', 'cobro')
    list_filter = ('estado', 'hora_entrada', 'vehiculo__zona_asignada')
    date_hierarchy = 'hora_entrada'
    raw_id_fields = ('vehiculo', 'empleado_entrada', 'empleado_salida')
    readonly_fields = ('tiempo_total',)

    def tiempo_total(self, obj):
        return obj.tiempo_total()
    tiempo_total.short_description = 'Tiempo Estacionado'

@admin.register(Tarifa)
class TarifaAdmin(admin.ModelAdmin):
    list_display = ('tipo_vehiculo', 'valor_por_hora', 'valor_por_dia', 'valor_minimo', 'aplica_descuento')
    list_editable = ('valor_por_hora', 'valor_por_dia', 'valor_minimo')

# Modelos nuevos con configuraciones avanzadas

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('user', 'telefono', 'cantidad_vehiculos')
    search_fields = ('user__username', 'user__first_name', 'user__last_name', 'telefono')
    
    def cantidad_vehiculos(self, obj):
        return obj.mis_vehiculos.count()
    cantidad_vehiculos.short_description = 'Vehículos Registrados'

@admin.register(Empleado)
class EmpleadoAdmin(admin.ModelAdmin):
    list_display = ('user', 'cargo', 'telefono', 'fecha_contratacion', 'activo')
    list_filter = ('cargo', 'fecha_contratacion')
    search_fields = ('user__username', 'user__first_name', 'user__last_name')
    
    def activo(self, obj):
        return obj.user.is_active
    activo.boolean = True

@admin.register(Incidente)
class IncidenteAdmin(admin.ModelAdmin):
    list_display = ('id', 'vehiculo', 'empleado', 'fecha', 'resuelto')
    list_filter = ('resuelto', 'fecha')
    actions = ['marcar_resueltos']
    
    def marcar_resueltos(self, request, queryset):
        queryset.update(resuelto=True)
    marcar_resueltos.short_description = "Marcar incidentes como resueltos"

@admin.register(Promocion)
class PromocionAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'descripcion', 'descuento', 'valido_desde', 'valido_hasta', 'activo')
    list_filter = ('activo',)
    search_fields = ('codigo', 'descripcion')
    
    def activo(self, obj):
        now = timezone.now()
        return obj.valido_desde <= now <= obj.valido_hasta
    activo.boolean = True

@admin.register(Pago)
class PagoAdmin(admin.ModelAdmin):
    list_display = ('id', 'registro_parqueo', 'monto', 'metodo_pago', 'estado', 'fecha_pago')
    list_filter = ('estado', 'metodo_pago', 'fecha_pago')
    readonly_fields = ('fecha_pago',)

@admin.register(Factura)
class FacturaAdmin(admin.ModelAdmin):
    list_display = ('id', 'pago', 'cliente', 'total', 'fecha_emision')
    readonly_fields = ('fecha_emision',)
    raw_id_fields = ('pago', 'cliente')