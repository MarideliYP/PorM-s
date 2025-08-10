from django.contrib import admin
from .models import Producto, Oferta, Evento, Reserva, CarroCompra, ArticuloCarro

# Register your models here.
admin.site.register([Producto, Oferta, Evento, Reserva, CarroCompra, ArticuloCarro])
