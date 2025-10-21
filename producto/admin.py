from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline
from .models import (
    Empresa, Producto, Inmueble, Oferta, Evento,
    Reserva, CarroCompra, ArticuloCarro,
    ContratoFirmado, Contrato, Valoracion, Media
)


class MediaInline(GenericTabularInline):
    model = Media
    extra = 1
    fields = ('tipo', 'archivo', 'orden')
    ordering = ('orden',)


@admin.register(Empresa)
class EmpresaAdmin(admin.ModelAdmin):
    inlines = [MediaInline]


@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    inlines = [MediaInline]


@admin.register(Inmueble)
class InmuebleAdmin(admin.ModelAdmin):
    inlines = [MediaInline]


@admin.register(Oferta)
class OfertaAdmin(admin.ModelAdmin):
    inlines = [MediaInline]


@admin.register(Evento)
class EventoAdmin(admin.ModelAdmin):
    inlines = [MediaInline]


admin.site.register([Reserva, CarroCompra, ArticuloCarro, ContratoFirmado, Contrato, Valoracion])
