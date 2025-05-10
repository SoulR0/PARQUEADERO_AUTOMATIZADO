from django.db import models
from django.contrib.auth.models import User

TIPOS_VEHICULO = [
    ('carro', 'Carro'),
    ('moto', 'Moto'),
    ('discapacitado', 'Discapacitado'),
]

ZONAS = [
    ('zona_carros', 'Zona Carros'),
    ('zona_motos', 'Zona Motos'),
    ('zona_discapacitados', 'Zona Discapacitados'),
]

class Zona(models.Model):
    nombre = models.CharField(max_length=50, choices=ZONAS, unique=True)
    capacidad = models.PositiveIntegerField()
    ocupados = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.nombre

class Vehiculo(models.Model):
    placa = models.CharField(max_length=10, unique=True)
    tipo = models.CharField(max_length=20, choices=TIPOS_VEHICULO)
    zona_asignada = models.ForeignKey(Zona, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.placa} - {self.tipo}"

class RegistroParqueo(models.Model):
    vehiculo = models.ForeignKey(Vehiculo, on_delete=models.CASCADE)
    hora_entrada = models.DateTimeField(auto_now_add=True)
    hora_salida = models.DateTimeField(null=True, blank=True)
    cobro = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)

    def tiempo_total(self):
        if self.hora_salida:
            return self.hora_salida - self.hora_entrada
        return None

class Tarifa(models.Model):
    tipo_vehiculo = models.CharField(max_length=20, choices=TIPOS_VEHICULO)
    valor_por_hora = models.DecimalField(max_digits=6, decimal_places=2)
    valor_por_dia = models.DecimalField(max_digits=6, decimal_places=2)
    valor_dia_festivo = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return f"Tarifa {self.tipo_vehiculo}"
from django.db import models
