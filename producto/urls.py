from django.urls import path
from .views import Producto_add, Producto_delete, Producto_update, Inmueble_add, Inmueble_delete, Inmueble_update,\
    Oferta_add,  Oferta_delete, Oferta_update, Evento_add,  Evento_delete, Evento_update, Reserva_add,\
    editar_reserva, eliminar_reserva, add_producto_carrito, add_oferta_carrito, ajustar_carrito_item, \
    eliminar_carrito_item, enviar_carrito, GestionarContratoView, SubirContratoFirmadoView, SubirContratoAdminView, \
    pedir_cuenta, buscar, evento_detalle, inmueble_detalle, producto_detalle, oferta_detalle, eliminar_valoracion, \
    editar_valoracion, crear_valoracion

app_name = 'producto'

urlpatterns = [
    path('buscar/', buscar, name='buscar'),
    path('inmueble/<int:pk>/valoracion/', crear_valoracion, name='crear_valoracion'),
    path('valoracion/<int:pk>/editarv/', editar_valoracion, name='editar_valoracion'),
    path('valoracion/<int:pk>/eliminarv/', eliminar_valoracion, name='eliminar_valoracion'),

    path('addp/', Producto_add.as_view(), name='addp'),
    path('<int:pk>/deletep/', Producto_delete.as_view(), name='deletep'),
    path('<int:pk>/updatep/', Producto_update.as_view(), name='updatep'),
    path('gestionar-contrato/', GestionarContratoView.as_view(), name='gestionar_contrato'),
    path('subir-contrato-admin/', SubirContratoAdminView.as_view(), name='subir_contrato_admin'),
    path('subir-contrato-firmado/', SubirContratoFirmadoView.as_view(), name='subir_contrato_firmado'),

    path('addi/', Inmueble_add.as_view(), name='addi'),
    path('<int:pk>/deletei/', Inmueble_delete.as_view(), name='deletei'),
    path('<int:pk>/updatei/', Inmueble_update.as_view(), name='updatei'),

    path('addo/', Oferta_add.as_view(), name='addo'),
    path('<int:pk>/deleteo/', Oferta_delete.as_view(), name='deleteo'),
    path('<int:pk>/updateo/', Oferta_update.as_view(), name='updateo'),

    path('adde/', Evento_add.as_view(), name='adde'),
    path('addr/<int:pk>/', Reserva_add.as_view(), name='addr'),
    path('<int:pk>/deleter/', eliminar_reserva, name='deleter'),
    path('<int:pk>/updater/', editar_reserva, name='updater'),
    path('<int:pk>/deletee/', Evento_delete.as_view(), name='deletee'),
    path('<int:pk>/updatee/', Evento_update.as_view(), name='updatee'),

    path('producto/<int:pk>/', producto_detalle, name='producto_detalle'),
    path('inmueble/<int:pk>/', inmueble_detalle, name='inmueble_detalle'),
    path('oferta/<int:pk>/', oferta_detalle, name='oferta_detalle'),
    path('evento/<int:pk>/', evento_detalle, name='evento_detalle'),

    # path("carrito/", carrito_view, name='carrito'),
    path('carrito_item/<int:pk>/ajustar/<str:tipo>/', ajustar_carrito_item, name='ajustar-carrito-item'),
    path('carrito_item/<int:pk>/eliminar/', eliminar_carrito_item, name='eliminar-carrito-item'),
    path('carrito_item/<int:pk>/addp/', add_producto_carrito, name='add_producto_carrito'),
    path('carrito_item/<int:pk>/addo/', add_oferta_carrito, name='add_oferta_carrito'),
    path('carrito_item/enviar_carrito/', enviar_carrito, name='enviar-carrito'),
    path('carrito_item/pedir_cuenta/', pedir_cuenta, name='pedir-cuenta'),
]

