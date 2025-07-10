from django.urls import path
from .views import Producto_add, Producto_delete, Producto_update, Oferta_add,  Oferta_delete, \
    Oferta_update, Evento_add,  Evento_delete, Evento_update, add_producto_carrito, ajustar_carrito_item, \
    eliminar_carrito_item, enviar_carrito, Evento_list, Oferta_list, Producto_list

app_name = 'producto'

urlpatterns = [
    path('addp/', Producto_add.as_view(), name='addp'),
    path('<int:pk>/deletep/', Producto_delete.as_view(), name='deletep'),
    path('<int:pk>/updatep/', Producto_update.as_view(), name='updatep'),

    path('addo/', Oferta_add.as_view(), name='addo'),
    path('<int:pk>/deleteo/', Oferta_delete.as_view(), name='deleteo'),
    path('<int:pk>/updateo/', Oferta_update.as_view(), name='updateo'),

    path('adde/', Evento_add.as_view(), name='adde'),
    path('<int:pk>/deletee/', Evento_delete.as_view(), name='deletee'),
    path('<int:pk>/updatee/', Evento_update.as_view(), name='updatee'),

    # path("carrito/", carrito_view, name='carrito'),
    path("carrito_item/<int:pk>/add/", add_producto_carrito, name='add_producto_carrito'),
    path("carrito_item/<int:pk>/eliminar/", eliminar_carrito_item, name='eliminar-carrito-item'),
    path("carrito_item/enviar_carrito/", enviar_carrito, name='enviar-carrito'),
    path("carrito_item/<int:pk>/ajustar/<str:tipo>/", ajustar_carrito_item, name='ajustar-carrito-item'),
]

