from django.shortcuts import redirect
from django.urls import path
from .views import producto_add, Producto_delete, Producto_update, Inmueble_add, Inmueble_delete, Inmueble_update, \
    Oferta_delete, Oferta_update, evento_add, Evento_delete, Evento_update, Reserva_add, \
    editar_reserva, eliminar_reserva, add_producto_carrito, add_oferta_carrito, ajustar_carrito_item, \
    eliminar_carrito_item, GestionarContratoView, SubirContratoFirmadoView, SubirContratoAdminView, \
    pedir_cuenta, buscar, evento_detalle, inmueble_detalle, producto_detalle, oferta_detalle, empresa_detalle, \
    eliminar_valoracion, editar_valoracion, crear_valoracion, ContratoFirmadoUpdate, contrato_firmado_delete, \
    Empresa_delete, Empresa_add, agregar_media, oferta_add, subir_pago, limpiar_reservas, vistarepartidor, marcar_pago

app_name = 'producto'

urlpatterns = [
    path('buscar/', buscar, name='buscar'),
    path('pago/<str:tipo>/<int:pk>/', subir_pago, name='subir_pago'),
    path('repartidor/', vistarepartidor, name='repartidor'),
    path('inmueble/<int:pk>/valoracion/', crear_valoracion, name='crear_valoracion'),
    path('valoracion/<int:pk>/editarv/', editar_valoracion, name='editar_valoracion'),
    path('valoracion/<int:pk>/eliminarv/', eliminar_valoracion, name='eliminar_valoracion'),
    path('media/agregar/<str:content_type_str>/<int:pk>/', agregar_media, name='agregar_media'),

    path('addp/', producto_add, name='addp'),
    path('addp/<int:empresa_pk>/', producto_add, name='addp-empresa'),
    path('<int:pk>/deletep/', Producto_delete.as_view(), name='deletep'),
    path('<int:pk>/updatep/', Producto_update.as_view(), name='updatep'),

    path('<int:pk>/deletec/', contrato_firmado_delete, name='deletec'),
    path('gestionar-contrato/<str:tipo>/', GestionarContratoView.as_view(), name='gestionar_contrato'),
    path('subir-contrato-admin/<str:tipo>/', SubirContratoAdminView.as_view(), name='subir_contrato_admin'),
    path('subir-contrato-firmado/<str:tipo>/', SubirContratoFirmadoView.as_view(), name='subir_contrato_firmado'),
    path('actualizar-contrato-firmado/<int:pk>/editarc/', ContratoFirmadoUpdate.as_view(), name='editarc'),

    path('addi/', Inmueble_add.as_view(), name='addi'),
    path('<int:pk>/deletei/', Inmueble_delete.as_view(), name='deletei'),
    path('<int:pk>/updatei/', Inmueble_update.as_view(), name='updatei'),

    path('addo/', oferta_add, {'empresa_pk': None}, name='addo'),
    path('addo/<int:empresa_pk>/', oferta_add, name='addo-empresa'),
    path('<int:pk>/deleteo/', Oferta_delete.as_view(), name='deleteo'),
    path('<int:pk>/updateo/', Oferta_update.as_view(), name='updateo'),

    path('addem/', Empresa_add.as_view(), name='addem'),
    path('empresa/<int:pk>/', empresa_detalle, name='empresa_detalle'),
    path('<int:pk>/deleteem/', Empresa_delete.as_view(), name='deleteem'),
    path('<int:pk>/updateem/', Inmueble_update.as_view(), name='updateem'),

    path('adde/', evento_add, name='adde'),
    path('adde/<int:empresa_pk>/', evento_add, name='adde-empresa'),
    path('<int:pk>/deletee/', Evento_delete.as_view(), name='deletee'),
    path('<int:pk>/updatee/', Evento_update.as_view(), name='updatee'),

    path('<int:pk>/updater/', editar_reserva, name='updater'),
    path('addr/<int:pk>/', Reserva_add.as_view(), name='addr'),
    path('<int:pk>/deleter/', eliminar_reserva, name='deleter'),
    path('limpiar-reservas/', limpiar_reservas, name='limpiar_reservas'),

    path('producto/<int:pk>/', producto_detalle, name='producto_detalle'),
    path('inmueble/<int:pk>/', inmueble_detalle, name='inmueble_detalle'),
    path('oferta/<int:pk>/', oferta_detalle, name='oferta_detalle'),
    path('evento/<int:pk>/', evento_detalle, name='evento_detalle'),

    # path("carrito/", carrito_view, name='carrito'),
    path('carrito_item/<int:pk>/ajustar/<str:tipo>/', ajustar_carrito_item, name='ajustar-carrito-item'),
    path('carrito_item/<int:pk>/eliminar/', eliminar_carrito_item, name='eliminar-carrito-item'),
    path('carrito_item/<int:pk>/addp/', add_producto_carrito, name='add_producto_carrito'),
    path('carrito_item/<int:pk>/addo/', add_oferta_carrito, name='add_oferta_carrito'),
    path('marcar-pago/<int:pk>/', marcar_pago, name='marcar_pago'),
    path('carrito_item/pedir_cuenta/', pedir_cuenta, name='pedir-cuenta'),

    path('ir/facebook/', lambda r: redirect('https://www.facebook.com/groups/723642505440410'), name='ir_facebook'),
]

