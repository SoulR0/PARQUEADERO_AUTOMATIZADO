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
    # --- Campos nuevos ---
    ubicacion = models.CharField(  # Ej: "Piso 1", "Sótano B"
        max_length=50,
        blank=True,
        null=True,
        help_text="Descripción física de la zona (piso, sector, etc.)"
    )
    tarifa_horaria = models.DecimalField(  # Tarifa específica por zona (anula Tarifa general si se usa)
        max_digits=6,
        decimal_places=2,
        null=True,
        blank=True
    )
    habilitada = models.BooleanField(default=True)  # Para desactivar zonas en mantenimiento

    def espacios_disponibles(self):
        return self.capacidad - self.ocupados

    def __str__(self):
        return f"{self.nombre} ({self.ubicacion})" if self.ubicacion else self.nombre

class Vehiculo(models.Model):
    placa = models.CharField(max_length=10, unique=True)
    tipo = models.CharField(max_length=20, choices=TIPOS_VEHICULO)
    zona_asignada = models.ForeignKey(Zona, on_delete=models.SET_NULL, null=True, blank=True)
    fecha_registro = models.DateTimeField(auto_now_add=True) 
    # --- Campos nuevos ---
    marca = models.CharField(max_length=50, blank=True, null=True)  # Ej: Toyota, Honda
    modelo = models.CharField(max_length=50, blank=True, null=True)  # Ej: Corolla, CR-V
    color = models.CharField(max_length=30, blank=True, null=True)
    cliente = models.ForeignKey(  # Dueño del vehículo (relación opcional)
        'Cliente',  # Asume que crearás el modelo Cliente
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='mis_vehiculos'
    )
    observaciones = models.TextField(blank=True, null=True)  # Notas adicionales

    def __str__(self):
        return f"{self.placa} - {self.tipo} ({self.marca})"

class RegistroParqueo(models.Model):
    vehiculo = models.ForeignKey(Vehiculo, on_delete=models.CASCADE)
    hora_entrada = models.DateTimeField(auto_now_add=True)
    hora_salida = models.DateTimeField(null=True, blank=True)
    zona = models.ForeignKey(Zona, on_delete=models.PROTECT, null=True, blank=True)
    notas = models.TextField(blank=True, default='')
    cobro = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    # --- Campos nuevos ---
    empleado_entrada = models.ForeignKey(  # Quién registró la entrada
        'Empleado',  # Asume que crearás el modelo Empleado
        on_delete=models.SET_NULL,
        null=True,
        related_name='registros_entrada'
    )
    empleado_salida = models.ForeignKey(  # Quién registró la salida
        'Empleado',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='registros_salida'
    )
    promocion = models.ForeignKey(  # Descuento aplicado (opcional)
        'Promocion',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    estado = models.CharField(  # Para flujos de trabajo complejos
        max_length=20,
        choices=[
            ('activo', 'Activo'),
            ('finalizado', 'Finalizado'),
            ('pendiente_pago', 'Pendiente de Pago'),
        ],
        default='activo'
    )

    def tiempo_total(self):
        if self.hora_entrada and self.hora_salida:
            return self.hora_salida - self.hora_entrada
        return "N/A"



    def calcular_cobro(self, tarifa):
        # Lógica para calcular el cobro basado en tarifas y tiempo
        pass

    def __str__(self):
        return f"Registro #{self.id} - {self.vehiculo.placa}"

class Tarifa(models.Model):
    tipo_vehiculo = models.CharField(max_length=20, choices=TIPOS_VEHICULO, unique=True)
    valor_por_hora = models.DecimalField(max_digits=6, decimal_places=2)
    valor_por_dia = models.DecimalField(max_digits=6, decimal_places=2)
    valor_dia_festivo = models.DecimalField(max_digits=6, decimal_places=2)
    # --- Campos nuevos ---
    valor_minimo = models.DecimalField(  # Cobro mínimo (ej: primera hora)
        max_digits=6,
        decimal_places=2,
        default=0.0
    )
    aplica_descuento = models.BooleanField(
        default=False,
        help_text="Si esta tarifa permite aplicar promociones"
    )
    descripcion = models.TextField(
        blank=True,
        help_text="Detalles adicionales de la tarifa"
    )

    def __str__(self):
        return f"Tarifa {self.tipo_vehiculo} - ${self.valor_por_hora}/hora"

class Cliente(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    telefono = models.CharField(max_length=15)
    direccion = models.TextField(blank=True)

    def __str__(self):
        return f"{self.user.get_full_name()}"

class Reserva(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    vehiculo = models.ForeignKey(Vehiculo, on_delete=models.CASCADE)
    zona = models.ForeignKey(Zona, on_delete=models.CASCADE)
    fecha_reserva = models.DateTimeField(auto_now_add=True)
    fecha_entrada = models.DateTimeField()
    fecha_salida_estimada = models.DateTimeField()
    estado = models.CharField(max_length=20, choices=[
        ('pendiente', 'Pendiente'),
        ('activa', 'Activa'),
        ('completada', 'Completada'),
        ('cancelada', 'Cancelada'),
    ], default='pendiente')

    def __str__(self):
        return f"Reserva {self.id} - {self.vehiculo.placa}"

class Pago(models.Model):
    METODO_PAGO_CHOICES = [
        ('efectivo', 'Efectivo'),
        ('tarjeta', 'Tarjeta'),
        ('transferencia', 'Transferencia'),
        ('app', 'Aplicación Móvil'),
    ]
    
    ESTADO_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('completado', 'Completado'),
        ('fallido', 'Fallido'),
        ('reembolsado', 'Reembolsado'),
    ]

    registro_parqueo = models.ForeignKey(
        'RegistroParqueo', 
        on_delete=models.CASCADE,
        related_name='pagos',
        verbose_name='Registro de Parqueo'
    )
    monto = models.DecimalField(
        max_digits=10,  # Aumentado a 10 para mayor flexibilidad
        decimal_places=2,
        verbose_name='Monto Pagado'
    )
    fecha_pago = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Fecha de Pago'
    )
    metodo_pago = models.CharField(
        max_length=20,
        choices=METODO_PAGO_CHOICES,
        default='efectivo',
        verbose_name='Método de Pago'
    )
    estado = models.CharField(
        max_length=20,
        choices=ESTADO_CHOICES,
        default='pendiente',
        verbose_name='Estado del Pago'
    )
    comprobante = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name='Número de Comprobante'
    )
    referencia_pago = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name='Referencia de Pago'
    )
    empleado = models.ForeignKey(
        'Empleado',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Empleado que registró'
    )

    class Meta:
        verbose_name = 'Pago'
        verbose_name_plural = 'Pagos'
        ordering = ['-fecha_pago']
        indexes = [
            models.Index(fields=['fecha_pago']),
            models.Index(fields=['estado']),
            models.Index(fields=['metodo_pago']),
        ]

    def __str__(self):
        return f"Pago #{self.id} - {self.monto} ({self.get_estado_display()})"

    def save(self, *args, **kwargs):
        # Validación automática al guardar
        if self.monto <= 0:
            raise ValueError("El monto debe ser mayor que cero")
        super().save(*args, **kwargs)

class Empleado(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    cargo = models.CharField(max_length=50, choices=[
        ('administrador', 'Administrador'),
        ('operador', 'Operador'),
        ('vigilante', 'Vigilante'),
    ])
    telefono = models.CharField(max_length=15)
    fecha_contratacion = models.DateField()

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.cargo}"

class Incidente(models.Model):
    vehiculo = models.ForeignKey(Vehiculo, on_delete=models.CASCADE)
    empleado = models.ForeignKey(Empleado, on_delete=models.CASCADE)
    descripcion = models.TextField()
    fecha = models.DateTimeField(auto_now_add=True)
    resuelto = models.BooleanField(default=False)

    def __str__(self):
        return f"Incidente {self.id} - {self.vehiculo.placa}"

class Promocion(models.Model):
    codigo = models.CharField(max_length=20, unique=True)
    descripcion = models.TextField()
    descuento = models.DecimalField(max_digits=5, decimal_places=2)  # Porcentaje o monto fijo
    valido_desde = models.DateTimeField()
    valido_hasta = models.DateTimeField()
    activo = models.BooleanField(default=True)

    def __str__(self):
        return f"Promoción {self.codigo}"

class Factura(models.Model):
    pago = models.OneToOneField(Pago, on_delete=models.CASCADE)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    fecha_emision = models.DateTimeField(auto_now_add=True)
    detalles = models.TextField()
    subtotal = models.DecimalField(max_digits=8, decimal_places=2)
    impuestos = models.DecimalField(max_digits=8, decimal_places=2)
    total = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return f"Factura {self.id} - {self.cliente.user.get_full_name()}"

class ConfiguracionSistema(models.Model):
    nombre_estacionamiento = models.CharField(max_length=100)
    direccion = models.TextField()
    telefono = models.CharField(max_length=15)
    email = models.EmailField()
    horario_apertura = models.TimeField()
    horario_cierre = models.TimeField()
    impuesto = models.DecimalField(max_digits=5, decimal_places=2)  # Porcentaje

    def __str__(self):
        return self.nombre_estacionamiento


from django.db import models