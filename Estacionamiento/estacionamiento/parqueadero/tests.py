from django.test import TestCase
from django.utils import timezone
from .models import Vehiculo, Zona, Tarifa, RegistroParqueo, Pago
from decimal import Decimal

class VehiculoTestCase(TestCase):
    def test_creacion_vehiculo(self):
        vehiculo = Vehiculo.objects.create(placa='ABC123', tipo='Carro')
        self.assertEqual(vehiculo.placa, 'ABC123')
        self.assertEqual(vehiculo.tipo, 'Carro')

class ZonaTestCase(TestCase):
    def test_creacion_zona(self):
        zona = Zona.objects.create(nombre='Zona A', capacidad=10)
        self.assertEqual(zona.nombre, 'Zona A')
        self.assertEqual(zona.capacidad, 10)

class TarifaTestCase(TestCase):
    def test_creacion_tarifa(self):
        tarifa = Tarifa.objects.create(tipo_vehiculo='Carro', valor_hora=Decimal('5000.00'))
        self.assertEqual(tarifa.tipo_vehiculo, 'Carro')
        self.assertEqual(tarifa.valor_hora, Decimal('5000.00'))

class RegistroParqueoTestCase(TestCase):
    def setUp(self):
        self.vehiculo = Vehiculo.objects.create(placa='XYZ789', tipo='Moto')
        self.zona = Zona.objects.create(nombre='Zona B', capacidad=5)

    def test_creacion_registro_parqueo(self):
        registro = RegistroParqueo.objects.create(vehiculo=self.vehiculo, zona=self.zona)
        self.assertEqual(registro.vehiculo.placa, 'XYZ789')
        self.assertEqual(registro.zona.nombre, 'Zona B')
        self.assertIsNone(registro.hora_salida)
        self.assertIsNotNone(registro.hora_entrada)

class PagoTestCase(TestCase):
    def setUp(self):
        self.vehiculo = Vehiculo.objects.create(placa='LMN456', tipo='Carro')
        self.zona = Zona.objects.create(nombre='Zona C', capacidad=8)
        self.registro = RegistroParqueo.objects.create(vehiculo=self.vehiculo, zona=self.zona)

    def test_creacion_pago(self):
        pago = Pago.objects.create(registro=self.registro, monto=Decimal('10000.00'))
        self.assertEqual(pago.registro, self.registro)
        self.assertEqual(pago.monto, Decimal('10000.00'))
        self.assertIsNotNone(pago.fecha_pago)




from django.test import TestCase
from .models import RegistroParqueo

