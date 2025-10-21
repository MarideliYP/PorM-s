import datetime
from user.models import User
from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey


class Empresa(models.Model):
    nombre = models.CharField(max_length=255)
    description = models.CharField(max_length=1000)
    image = models.ImageField(upload_to='empresas/')


TIPO_CONTRATO_CHOICES = [
    ('empresa', 'Contrato de Empresa'),
    ('inmueble', 'Contrato de Inmueble'),
]


class Contrato(models.Model):
    archivo = models.FileField(upload_to='contratos/')
    activo = models.BooleanField(default=False)
    tipo = models.CharField(max_length=20, choices=TIPO_CONTRATO_CHOICES)
    fecha_subida = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.get_tipo_display()} (activo: {self.activo})"


class ContratoFirmado(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    archivo = models.FileField(upload_to='contratos_firmados/')
    tipo = models.CharField(max_length=20, choices=TIPO_CONTRATO_CHOICES)
    estado = models.CharField(max_length=20, default='pendiente')  # pendiente, confirmado
    fecha_subida = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Contrato firmado por {self.usuario} - {self.get_tipo_display()}"


class Media(models.Model):
    TIPO_CHOICES = [
        ('imagen', 'Imagen'),
        ('video', 'Video'),
    ]

    # Relación genérica
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES)
    archivo = models.FileField(upload_to='media/')
    orden = models.PositiveIntegerField(default=1)

    class Meta:
        ordering = ['orden', 'pk']

    def __str__(self):
        return f"{self.get_tipo_display()} - {self.content_object or 'Sin objeto'}"


class Producto(models.Model):
    nombreP = models.CharField(max_length=255)
    detalles = models.CharField(max_length=500)
    image = models.ImageField(upload_to='productos/')
    precio = models.DecimalField(max_digits=5, decimal_places=2)
    tipos = (
        ('turismo', 'Turismo'),
        ('comidas-bebidas', 'Comidas y bebidas'),
        ('articulo-hogar', 'Articulos del hogar'),
        ('belleza', 'Belleza'),
    )
    tipo = models.CharField(max_length=21, choices=tipos)
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, related_name="producto", null=True, blank=True)

    def __str__(self) -> str:
        return f'{self.nombreP}'


class Inmueble(models.Model):
    nombreI = models.CharField(max_length=255)
    detalles = models.CharField(max_length=1000)
    image = models.ImageField(upload_to='inmuebles/')
    numagente = models.IntegerField(default=53957442)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    tipos = (
        ('arroyo_naranjo', 'Arroyo Naranjo'),
        ('boyeros', 'Boyeros'),
        ('cerro', 'Cerro'),
        ('cotorro', 'Cotorro'),
        ('diez_de_octubre', 'Diez de Octubre'),
        ('guanabacoa', 'Guanabacoa'),
        ('habana_del_este', 'La Habana del Este'),
        ('habana_vieja', 'La Habana Vieja'),
        ('la Lisa', 'La Lisa'),
        ('marianao', 'Marianao'),
        ('playa', 'Playa'),
        ('plaza', 'Plaza de la Revolución'),
        ('regla', 'Regla'),
        ('san_miguel_del_padron', 'San Miguel del Padrón'),
    )
    tipo = models.CharField(max_length=21, choices=tipos)

    def __str__(self) -> str:
        return f'{self.nombreI}'


class Oferta(models.Model):
    nombreO = models.CharField(max_length=255)
    description = models.CharField(max_length=500)
    image = models.ImageField(upload_to='ofertas/')
    precio = models.DecimalField(max_digits=5, decimal_places=2)
    tipos = (
        ('marketimg', 'Marketing Digital'),
        ('promocion', 'Promoción y Publicidad'),
        ('carteles', 'Diseño de Carteles y Fotos'),
        ('gestion', 'Gestión de Compra y Venta Inmobiliaria'),
    )
    tipo = models.CharField(max_length=15, choices=tipos)
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, related_name="oferta", null=True, blank=True)

    def __str__(self) -> str:
        return f'{self.nombreO}'


class Evento(models.Model):
    nombreE = models.CharField(max_length=255)
    description = models.CharField(max_length=500)
    image = models.ImageField(upload_to='eventos/')
    capacidad = models.IntegerField(default=1)
    fechahora = models.DateTimeField(default=datetime.datetime.now)
    preciocover = models.DecimalField(max_digits=5, decimal_places=2)
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, related_name="evento", null=True, blank=True)

    def __str__(self) -> str:
        return f'{self.nombreE}'


class Reserva(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reserva")
    evento = models.ForeignKey(Evento, on_delete=models.CASCADE, related_name="reserva")
    num_personas = models.IntegerField(default=1)
    num_confirm = models.IntegerField(default=0)
    pagar = models.ImageField(upload_to='reservas/', null=True)
    estado = models.BooleanField(default=False)
    mensaje = models.CharField(max_length=1000, null=True, blank=True)

    def get_total(self):
        return self.evento.preciocover * self.num_personas


class CarroCompra(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name="carritos")
    pagar = models.ImageField(upload_to='carrosCompra/', null=True)
    fecha_pago = models.DateTimeField(null=True, blank=True)
    fecha_envio = models.DateTimeField(null=True, blank=True)
    pagado = models.BooleanField(default=False)
    cerrado = models.BooleanField(default=False)

    def precio_total(self):
        items = self.items.all()
        suma = 0
        for item in items:
            if item.producto is not None:
                suma += item.producto.precio * item.cantidad
            elif item.oferta is not None:
                suma += item.oferta.precio * item.cantidad
        return suma

    def __str__(self) -> str:
        return f'{self.usuario}-{self.pk}'


class ArticuloCarro(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name="items", null=True, blank=True)
    oferta = models.ForeignKey(Oferta, on_delete=models.CASCADE, related_name="items", null=True, blank=True)
    reserva = models.ForeignKey(Reserva, on_delete=models.CASCADE, related_name="items", null=True, blank=True)
    carrito = models.ForeignKey(CarroCompra, on_delete=models.CASCADE, related_name="items")
    cantidad = models.PositiveIntegerField(default=0)

    def __str__(self):
        if self.producto is not None:
            return f'{self.producto.nombreP}'
        elif self.oferta is not None:
            return f'{self.oferta.nombreO}'
        else:
            return f'{self.reserva.evento.nombreE}'


class Valoracion(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name="valoraciones")
    evento = models.ForeignKey(Evento, on_delete=models.CASCADE, related_name='valoraciones', null=True, blank=True)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name='valoraciones', null=True, blank=True)
    inmueble = models.ForeignKey(Inmueble, on_delete=models.CASCADE, related_name='valoraciones', null=True, blank=True)
    oferta = models.ForeignKey(Oferta, on_delete=models.CASCADE, related_name='valoraciones', null=True, blank=True)
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, related_name="valoraciones", null=True, blank=True)

    valor = models.PositiveSmallIntegerField(choices=[(i, i) for i in range(1, 6)])
    comentario = models.TextField(max_length=1000, blank=True)
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.usuario} - {self.valor}★"
