from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Zona, Vehiculo, RegistroParqueo, Tarifa

admin.site.register(Zona)
admin.site.register(Vehiculo)
admin.site.register(RegistroParqueo)
admin.site.register(Tarifa)