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


from django.test import TestCase, Client
from django.urls import reverse
from .models import Vehiculo, Zona, Tarifa, RegistroParqueo, Pago
from decimal import Decimal

class VehiculoViewsTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_crear_vehiculo_view(self):
        response = self.client.post(reverse('crear_vehiculo'), {
            'placa': 'TEST123',
            'tipo': 'Carro',
        })
        self.assertEqual(response.status_code, 302)  # redirige después de crear
        self.assertEqual(Vehiculo.objects.count(), 1)

    def test_listar_vehiculos_view(self):
        Vehiculo.objects.create(placa='ABC123', tipo='Moto')
        response = self.client.get(reverse('listar_vehiculos'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'ABC123')

class ZonaViewsTest(TestCase):
    def test_crear_zona_view(self):
        response = self.client.post(reverse('crear_zona'), {
            'nombre': 'Zona A',
            'capacidad': 20,
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Zona.objects.count(), 1)

    def test_listar_zonas_view(self):
        Zona.objects.create(nombre='Zona B', capacidad=15)
        response = self.client.get(reverse('listar_zonas'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Zona B')

class TarifaViewsTest(TestCase):
    def test_crear_tarifa_view(self):
        response = self.client.post(reverse('crear_tarifa'), {
            'tipo_vehiculo': 'Carro',
            'valor_hora': '6000.00',
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Tarifa.objects.count(), 1)

    def test_listar_tarifas_view(self):
        Tarifa.objects.create(tipo_vehiculo='Moto', valor_hora=Decimal('3000.00'))
        response = self.client.get(reverse('listar_tarifas'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Moto')

class RegistroParqueoViewsTest(TestCase):
    def setUp(self):
        self.vehiculo = Vehiculo.objects.create(placa='XYZ789', tipo='Carro')
        self.zona = Zona.objects.create(nombre='Zona C', capacidad=5)

    def test_crear_registro_view(self):
        response = self.client.post(reverse('crear_registro'), {
            'vehiculo': self.vehiculo.id,
            'zona': self.zona.id,
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(RegistroParqueo.objects.count(), 1)

class PagoViewsTest(TestCase):
    def setUp(self):
        self.vehiculo = Vehiculo.objects.create(placa='PAG123', tipo='Carro')
        self.zona = Zona.objects.create(nombre='Zona P', capacidad=3)
        self.registro = RegistroParqueo.objects.create(vehiculo=self.vehiculo, zona=self.zona)

    def test_crear_pago_view(self):
        response = self.client.post(reverse('crear_pago'), {
            'registro': self.registro.id,
            'monto': '10000.00',
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Pago.objects.count(), 1)




from django.test import TestCase
from .models import RegistroParqueo

