from django.urls import path
from . import views

urlpatterns = [
    # Páginas principales
    path('', views.dashboard, name='dashboard'),
    path('inicio/', views.mi_vista, name='inicio'),  # Manteniendo tu vista original como alternativa
    
    # Gestión de vehículos
    path('vehiculos/', views.lista_vehiculos, name='lista_vehiculos'),
    path('vehiculos/agregar/', views.agregar_vehiculo, name='agregar_vehiculo'),
 #   path('vehiculos/<int:vehiculo_id>/', views.detalle_vehiculo, name='detalle_vehiculo'),
    
    # Operaciones de parqueo
    path('registro/entrada/', views.registro_entrada, name='registro_entrada'),
    path('registro/salida/<int:registro_id>/', views.registrar_salida, name='registrar_salida'),
    path('registros/activos/', views.api_registros_activos, name='registros_activos'),
    path('registros/historial/', views.api_historial_registros, name='historial_registros'),

    # Gestión de pagos
    path('pagos/', views.gestion_pagos, name='gestion_pagos'),
    path('pagos/nuevo/<int:registro_id>/', views.crear_pago, name='crear_pago'),
    path('pagos/historial/', views.historial_pagos, name='historial_pagos'),
    
    # Gestión de zonas
    path('zonas/', views.lista_zonas, name='lista_zonas'),
    path('zonas/<int:zona_id>/', views.detalle_zona, name='detalle_zona'),
    
    # API (si necesitas endpoints para frontend moderno)
    path('api/registros/', views.lista_registros_parqueo, name='api_registros'),
    path('api/zonas/disponibles/', views.api_zonas_disponibles, name='api_zonas_disponibles'),

]


