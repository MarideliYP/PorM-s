import os

from django.contrib.contenttypes.models import ContentType
# import openpyxl
from django.core.exceptions import PermissionDenied
from django.views import View
from .models import Producto, Inmueble, Oferta, Evento, Reserva, CarroCompra, ArticuloCarro, Valoracion, Contrato, \
    ContratoFirmado, Empresa, Media
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.urls import reverse, reverse_lazy
from datetime import datetime
from django.contrib import messages
from django.utils.decorators import method_decorator
from .forms import Producto_form, Inmueble_form, Oferta_form, Evento_form, Reserva_form, Empresa_form, \
    MediaForm
# from openpyxl import load_workbook
from django.views.generic import (
    UpdateView,
    CreateView,
    DeleteView,
    ListView, TemplateView,
)


def es_empresa(user):
    return user.groups.filter(name='Empresa').exists()


def es_admin(user):
    return user.groups.filter(name='Administrador').exists()


def es_cliente(user):
    return user.groups.filter(name='Cliente').exists()


def es_repartidor(user):
    return user.groups.filter(name='Repartidor').exists()


def es_admin_o_cliente(user):
    return user.groups.filter(name__in=['Administrador', 'Cliente']).exists()


def es_flotante(user):
    return user.groups.filter(name='Cliente').exists()


def vistaprincipal(request):
    # Verificar roles del usuario
    is_administrador = request.user.is_staff
    is_cliente = request.user.groups.filter(name='Cliente').exists()
    is_repartidor = request.user.groups.filter(name='Repartidor').exists()
    is_empresa = request.user.groups.filter(name='Empresa').exists()

    context = {
        'productos': Producto.objects.all(),
        'inmuebles': Inmueble.objects.all(),
        'empresas': Empresa.objects.all(),
        'ofertas': Oferta.objects.all(),
        'eventos': Evento.objects.all(),
        'is_Administrador': is_administrador,
        'is_Cliente': is_cliente,
        'is_Repartidor': is_repartidor,
        'is_Empresa': is_empresa,
        'contratos': [],
        'reservas': [],
    }

    if request.user.is_authenticated:
        reservas = Reserva.objects.filter(usuario=request.user)
        context['reservas'] = reservas

        contratos = ContratoFirmado.objects.filter(usuario=request.user)
        context['contratos'] = contratos

        # Manejo del carrito
        carritos = CarroCompra.objects.filter(usuario=request.user, pagado=False, cerrado=False)
        if carritos.exists():
            carrito = carritos.first()
        else:
            carrito = CarroCompra.objects.create(usuario=request.user)

        # Calcular cuenta pendiente de envío (carritos enviados pero no pagados)
        enviados = CarroCompra.objects.filter(usuario=request.user, pagado=True, cerrado=False)
        cuenta_total = sum(carrito.precio_total() for carrito in enviados)

        context.update({
            'enviados': enviados.exists(),
            'cuenta_total': cuenta_total,
            'carrito': carrito,
            'precio_total': carrito.precio_total(),
            'articulos': carrito.items.all(),
            'reserva_forms': [(reserva, Reserva_form(instance=reserva)) for reserva in context['reservas']],

        })

    return render(request, 'index.html', context)


def buscar(request):
    context = {
        'productos': [],
        'ofertas': [],
        'eventos': [],
        'inmuebles': []
    }

    nombre = request.POST.get('buscar_nombre', '').strip()

    if nombre:
        # Filtrar solo si hay texto
        context['productos'] = Producto.objects.filter(nombreP__icontains=nombre)
        context['ofertas'] = Oferta.objects.filter(nombreO__icontains=nombre)
        context['eventos'] = Evento.objects.filter(nombreE__icontains=nombre)
        context['inmuebles'] = Inmueble.objects.filter(nombreI__icontains=nombre)

    # Pasar el término buscado para mostrarlo
    context['termino'] = nombre

    return render(request, 'buscar.html', context)


ALLOWED_MODELS = {
    'producto': Producto,
    'inmueble': Inmueble,
    'oferta': Oferta,
    'evento': Evento,
    'empresa': Empresa,
}


def agregar_media(request, content_type_str, pk):
    # Validar tipo de contenido
    if content_type_str not in ALLOWED_MODELS:
        messages.error(request, "Tipo de objeto no permitido.")
        return redirect('index')

    content_type = get_object_or_404(ContentType, model=content_type_str)
    obj = get_object_or_404(content_type.model_class(), pk=pk)
    print('object: ', obj)

    if request.method == 'POST':
        form = MediaForm(request.POST, request.FILES)
        if form.is_valid():
            media = form.save(commit=False)
            media.content_object = obj
            print('media: ', media)

            media.save()
            messages.success(request, f"Media añadida a {obj}.")
            return redirect('producto:' + content_type_str + '_detalle', pk=pk)
    else:
        form = MediaForm()

    return render(request, 'media.html', {
        'form': form,
        'obj': obj,
        'content_type_str': content_type_str,
    })


@method_decorator(login_required, name='dispatch')
class Producto_add(CreateView):
    template_name = 'producto/add_producto.html'
    model = Producto
    form_class = Producto_form

    def get_success_url(self):
        return reverse('index')


@method_decorator(login_required, name='dispatch')
class Producto_update(UpdateView):
    template_name = 'producto/actualizar_producto.html'
    queryset = Producto.objects.all()
    form_class = Producto_form

    def get_success_url(self):
        return reverse('index')


@method_decorator(login_required, name='dispatch')
class Producto_list(ListView):
    queryset = Producto.objects.all()
    template_name = 'producto/producto_list.html'


@method_decorator(login_required, name='dispatch')
class Producto_delete(DeleteView):
    template_name = 'producto/eliminar_producto.html'
    queryset = Producto.objects.all()

    def get_success_url(self):
        return reverse("index")


class SubirContratoFirmadoView(View):
    def post(self, request):
        archivo = request.FILES.get('archivo')
        allowed_extensions = ['.jpg', '.pdf']
        ext = os.path.splitext(archivo.name)[1].lower()
        if not archivo:
            messages.error(request, "Selecciona un archivo.")
        elif ext not in allowed_extensions:
            messages.error(request, "Solo se permiten PDFs o JPGs.")
        else:
            Contrato.objects.filter(activo=True).update(activo=False)
            contrato_firmado = ContratoFirmado(usuario=request.user, archivo=archivo)
            contrato_firmado.save()
            messages.success(request, "Contrato firmado subido con éxito.")
        return redirect('producto:gestionar_contrato')


@method_decorator(login_required, name='dispatch')
class ContratoFirmadoUpdate(UpdateView):
    model = ContratoFirmado
    fields = ['archivo']  # Solo el archivo es parte del ModelForm
    success_url = reverse_lazy('index')

    def get_object(self, queryset=None):
        contrato = get_object_or_404(ContratoFirmado, pk=self.kwargs['pk'])
        if contrato.usuario != self.request.user and not self.request.user.is_staff:
            raise PermissionDenied
        return contrato

    def form_valid(self, form):
        contrato = self.get_object()
        nuevo_archivo = form.cleaned_data.get('archivo')

        # 1. ✅ Eliminar archivo anterior si se sube uno nuevo
        if nuevo_archivo and contrato.archivo and os.path.isfile(contrato.archivo.path):
            os.remove(contrato.archivo.path)

        # 2. ✅ Actualizar `estado` solo si el usuario es staff y el checkbox está marcado
        if self.request.user.is_staff:
            contrato.estado = 'confirmado' in self.request.POST  # True si está marcado
            contrato.save()  # ← Importante: guardar el estado

        messages.success(self.request, "Contrato actualizado correctamente.")
        return redirect(self.success_url)

    def form_invalid(self, form):
        messages.error(self.request, "Hubo un error al actualizar el contrato.")
        return super().form_invalid(form)


@login_required
def contrato_firmado_delete(request, pk):
    contrato = get_object_or_404(ContratoFirmado, pk=pk, usuario=request.user)
    pku = contrato.usuario.pk

    if request.method == 'POST':
        if contrato.archivo and os.path.isfile(contrato.archivo.path):
            os.remove(contrato.archivo.path)
        contrato.delete()
        messages.success(request, "Contrato firmado eliminado correctamente.")
    return redirect('user:details', pk=pku)


@method_decorator(login_required, name='dispatch')
class SubirContratoAdminView(View):
    def post(self, request):
        if not request.user.is_staff:
            raise PermissionDenied

        archivo = request.FILES.get('archivo')
        allowed_extensions = ['.jpg', '.pdf']
        ext = os.path.splitext(archivo.name)[1].lower()

        if not archivo:
            messages.error(request, "Selecciona un archivo.")
        elif ext not in allowed_extensions:
            messages.error(request, "Solo se permiten PDFs o JPGs.")
        else:
            Contrato.objects.filter(activo=True).update(activo=False)
            nuevo = Contrato(archivo=archivo, activo=True)
            nuevo.save()
            messages.success(request, "Nuevo contrato oficial subido.")
        return redirect('producto:gestionar_contrato')

    def get(self, request):
        if not request.user.is_staff:
            return redirect('producto:gestionar_contrato')
        return redirect('producto:gestionar_contrato')


@method_decorator(login_required, name='dispatch')
class GestionarContratoView(TemplateView):
    template_name = 'producto/gestionar_contrato.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['contrato'] = Contrato.objects.filter(activo=True).first()
        return context


@method_decorator(login_required, name='dispatch')
class Inmueble_add(CreateView):
    template_name = 'inmueble/add_inmueble.html'
    model = Inmueble
    form_class = Inmueble_form

    def get_success_url(self):
        return reverse('index')


@method_decorator(login_required, name='dispatch')
class Inmueble_update(UpdateView):
    template_name = 'inmueble/actualizar_inmueble.html'
    queryset = Inmueble.objects.all()
    form_class = Inmueble_form

    def get_success_url(self):
        return reverse('index')


@method_decorator(login_required, name='dispatch')
class Inmueble_list(ListView):
    queryset = Inmueble.objects.all()
    template_name = 'inmueble/inmueble_list.html'


@method_decorator(login_required, name='dispatch')
class Inmueble_delete(DeleteView):
    template_name = 'inmueble/eliminar_inmueble.html'
    queryset = Inmueble.objects.all()

    def get_success_url(self):
        return reverse("index")


@method_decorator(login_required, name='dispatch')
class Empresa_add(CreateView):
    model = Empresa
    form_class = Empresa_form
    template_name = 'empresa/add_empresa.html'
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        return super().form_valid(form)


@method_decorator(login_required, name='dispatch')
class Empresa_delete(DeleteView):
    template_name = 'empresa/eliminar_empresa.html'
    queryset = Empresa.objects.all()

    def get_success_url(self):
        return reverse("index")


@login_required
def oferta_add(request, empresa_pk=None):
    if request.method == "POST":
        form = Oferta_form(request.POST, request.FILES)
        if form.is_valid():

            oferta = form.save(commit=False)
            if empresa_pk:
                oferta.empresa = Empresa.objects.get(pk=empresa_pk)
                oferta.save()
                return redirect("producto:empresa_detalle", empresa_pk)

            oferta.save()
            return redirect('index')
    else:
        form = Oferta_form()

    context = {'form': form}

    return render(request, "oferta/add_oferta.html", context)


@method_decorator(login_required, name='dispatch')
class Oferta_update(UpdateView):
    template_name = 'oferta/actualizar_oferta.html'
    queryset = Oferta.objects.all()
    form_class = Oferta_form

    def get_success_url(self):
        return reverse('index')


@method_decorator(login_required, name='dispatch')
class Oferta_list(ListView):
    queryset = Oferta.objects.all()
    template_name = 'oferta/oferta_list.html'


@method_decorator(login_required, name='dispatch')
class Oferta_delete(DeleteView):
    template_name = 'oferta/eliminar_oferta.html'
    queryset = Oferta.objects.all()

    def get_success_url(self):
        return reverse("index")


@method_decorator(login_required, name='dispatch')
class Evento_add(CreateView):
    template_name = 'Evento/add_evento.html'
    queryset = Evento.objects.all()
    form_class = Evento_form

    def get_success_url(self):
        return reverse('index')


@method_decorator(login_required, name='dispatch')
class Evento_update(UpdateView):
    template_name = 'evento/actualizar_evento.html'
    queryset = Evento.objects.all()
    form_class = Evento_form

    def get_success_url(self):
        return reverse('index')


@method_decorator(login_required, name='dispatch')
class Evento_list(ListView):
    queryset = Evento.objects.all()
    template_name = 'evento/evento_list.html'


@method_decorator(login_required, name='dispatch')
class Evento_delete(DeleteView):
    template_name = 'evento/eliminar_evento.html'
    queryset = Evento.objects.all()

    def get_success_url(self):
        return reverse("index")


@method_decorator(login_required, name='dispatch')
class Reserva_add(CreateView):
    template_name = 'Evento/add_reserva.html'
    form_class = Reserva_form
    success_url = reverse_lazy('index')  # Cambia si quieres redirigir a otra página

    def form_valid(self, form):
        evento_id = self.kwargs.get('pk')
        evento = get_object_or_404(Evento, pk=evento_id)

        # Asignar usuario y evento
        form.instance.usuario = self.request.user
        form.instance.evento = evento

        # Si el usuario no es staff ni superusuario, forzar estado=False
        if not self.request.user.is_staff and not self.request.user.is_superuser:
            form.instance.estado = False

        messages.success(
            self.request,
            f"✅ Reserva creada con éxito para '{evento.nombreE}'."
        )
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(
            self.request,
            "❌ Por favor corrige los errores del formulario."
        )
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        evento_id = self.kwargs.get('pk')
        context['evento'] = get_object_or_404(Evento, pk=evento_id)
        return context


@login_required
def editar_reserva(request, pk):
    reserva = get_object_or_404(Reserva, pk=pk, usuario=request.user)
    pku = reserva.usuario.pk
    # No se puede editar si ya está confirmada
    if reserva.estado:
        messages.warning(
            request,
            "⚠️ No puedes editar una reserva que ya ha sido confirmada."
        )
        return redirect('index')

    if request.method == 'POST':
        num_personas = request.POST.get('num_personas')

        # Validar que sea un número
        if not num_personas or not num_personas.isdigit():
            messages.error(request, "❌ La cantidad de personas debe ser un número válido.")
        else:
            num_personas = int(num_personas)
            if num_personas < 1:
                messages.error(request, "❌ Debes reservar al menos 1 persona.")
            elif num_personas > 10:
                messages.error(request, "❌ Máximo 10 personas por reserva.")
            else:
                reserva.num_personas = num_personas
                reserva.save()
                messages.success(
                    request,
                    f"✅ Reserva actualizada: {num_personas} persona(s) para '{reserva.evento.nombreE}'."
                )
        if request.user.is_staff:
            return redirect('user:details', pk=pku)
        else:
            return redirect('index')
    return redirect('index')


@login_required
def eliminar_reserva(request, pk):
    reserva = get_object_or_404(Reserva, pk=pk, usuario=request.user)
    pku = reserva.usuario.pk

    if reserva.estado:
        messages.warning(
            request,
            "No puedes eliminar una reserva ya confirmada."
        )
    else:
        evento_nombre = reserva.evento.nombreE
        reserva.delete()
        messages.success(
            request,
            f"Reserva eliminada con éxito para '{evento_nombre}'."
        )

    if request.user.is_staff:
        return redirect('user:details', pk=pku)
    else:
        return redirect('index')


@method_decorator(login_required, name='dispatch')
class Reserva_list(ListView):
    queryset = Reserva.objects.all()
    template_name = 'evento/reserva_list.html'


@method_decorator(login_required, name='dispatch')
class Reserva_delete(DeleteView):
    template_name = 'evento/eliminar_reserva.html'
    queryset = Reserva.objects.all()

    def get_success_url(self):
        return reverse("index")


def producto_detalle(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    valoraciones = producto.valoraciones.all().order_by('-fecha')

    if request.method == 'POST':
        if not request.user.is_authenticated:
            return redirect('login')
        valor = request.POST.get('valor')
        comentario = request.POST.get('comentario', '')
        Valoracion.objects.create(
            usuario=request.user,
            producto=producto,
            valor=valor,
            comentario=comentario
        )
        messages.success(request, 'Gracias por tu valoración.')
        return redirect('producto:producto_detalle', pk=pk)

    return render(request, 'detalles/producto_detalle.html', {
        'producto': producto,
        'valoraciones': valoraciones
    })


def inmueble_detalle(request, pk):
    inmueble = get_object_or_404(Inmueble, pk=pk)
    valoraciones = inmueble.valoraciones.all().order_by('-fecha')

    if request.method == 'POST':
        if not request.user.is_authenticated:
            return redirect('login')
        valor = request.POST.get('valor')
        comentario = request.POST.get('comentario', '')
        Valoracion.objects.create(
            usuario=request.user,
            inmueble=inmueble,
            valor=valor,
            comentario=comentario
        )
        messages.success(request, 'Gracias por tu opinión.')
        return redirect('producto:inmueble_detalle', pk=pk)

    return render(request, 'detalles/inmueble_detalle.html', {
        'inmueble': inmueble,
        'valoraciones': valoraciones
    })


def oferta_detalle(request, pk):
    oferta = get_object_or_404(Oferta, pk=pk)
    valoraciones = oferta.valoraciones.all().order_by('-fecha')

    if request.method == 'POST':
        if not request.user.is_authenticated:
            return redirect('login')
        valor = request.POST.get('valor')
        comentario = request.POST.get('comentario', '')
        Valoracion.objects.create(
            usuario=request.user,
            oferta=oferta,
            valor=valor,
            comentario=comentario
        )
        messages.success(request, '¡Tu opinión ha sido enviada!')
        return redirect('producto:oferta_detalle', pk=pk)

    return render(request, 'detalles/oferta_detalle.html', {
        'oferta': oferta,
        'valoraciones': valoraciones
    })


def evento_detalle(request, pk):
    evento = get_object_or_404(Evento, pk=pk)
    valoraciones = evento.valoraciones.all().order_by('-fecha')
    media = Media.objects.filter(evento=evento)

    if request.method == 'POST':
        if not request.user.is_authenticated:
            return redirect('login')
        valor = request.POST.get('valor')
        comentario = request.POST.get('comentario', '')
        Valoracion.objects.create(
            usuario=request.user,
            evento=evento,
            valor=valor,
            comentario=comentario
        )
        messages.success(request, 'Gracias por tu feedback.')
        return redirect('producto:evento_detalle', pk=pk)

    return render(request, 'detalles/evento_detalle.html', {
        'evento': evento,
        'valoraciones': valoraciones,
        'media': media,
    })


def empresa_detalle(request, pk):
    empresa = get_object_or_404(Empresa, pk=pk)
    valoraciones = empresa.valoraciones.all().order_by('-fecha')

    content_type = ContentType.objects.get_for_model(Empresa)

    medias = Media.objects.filter(
        content_type=content_type,
        object_id=empresa.pk
    ).order_by('orden', 'pk')

    if request.method == 'POST':
        if not request.user.is_authenticated:
            return redirect('login')
        valor = request.POST.get('valor')
        comentario = request.POST.get('comentario', '')
        Valoracion.objects.create(
            usuario=request.user,
            empresa=empresa,
            valor=valor,
            comentario=comentario
        )
        messages.success(request, 'Gracias por tu feedback.')
        return redirect('producto:evento_detalle', pk=pk)

    return render(request, 'detalles/empresa_detalle.html', {
        'empresa': empresa,
        'eventos': empresa.evento.all(),
        'ofertas': empresa.oferta.all(),
        'productos': empresa.producto.all(),
        'valoraciones': valoraciones,
        'medias': medias
    })


# def export_venta_to_excel(carrito):
#     # Establecer el nombre del archivo Excel con la fecha de envío del carrito
#     file_name = f"ventas {carrito.fecha_envio.strftime('%m-%y')}.xlsx"
#
#     # Establecer el directorio donde se guardará el archivo Excel
#     dir_name = 'registros de ventas'
#
#     # Crear el directorio si no existe
#     if not os.path.exists(dir_name):
#         os.makedirs(dir_name)
#
#     # Establecer la ruta completa del archivo Excel
#     file_path = os.path.join(dir_name, file_name)
#
#     # Verificar si el archivo Excel existe
#     if os.path.exists(file_path):
#         # Cargar el archivo Excel existente
#         wb = load_workbook(file_path)
#     else:
#         # Crear un nuevo archivo Excel si no existe
#         wb = openpyxl.Workbook()
#         ws = wb.active
#
#         # Establecer los títulos de las columnas
#         ws['A1'] = 'Cliente'
#         ws['B1'] = 'Fecha'
#         ws['C1'] = 'Orden'
#         ws['D1'] = 'Precio'
#
#     # Seleccionar la hoja de trabajo activa
#     ws = wb.active
#
#     # Leer la última fila escrita en el archivo Excel
#     last_row = ws.max_row
#
#     # Establecer la fila inicial para escribir nuevos datos
#     row_num = last_row + 1 if last_row is not None else 1
#
#     # crear un str orden con todos los articulos dentro del carrito separados por coma
#     orden = ', '.join(str(item.cantidad) + ' ' + str(item) for item in carrito.items.all()).rstrip(', ')
#
#     # Escribir la venta en el archivo Excel
#     ws[f'A{row_num}'] = carrito.usuario.username
#     ws[f'B{row_num}'] = carrito.fecha_envio.replace(tzinfo=None)
#     ws[f'C{row_num}'] = orden
#     ws[f'D{row_num}'] = carrito.precio_total()
#     row_num += 1
#
#     # Guardar los cambios en el archivo Excel
#     wb.save(file_path)


# @login_required()
# def vistarepartidor(request):
#     context = {
#         'carritos': CarroCompra.objects.filter(enviado=True, pagado=False).order_by('fecha_envio'),
#         'is_Repartidor': True,
#     }
#     if request.method == 'POST':
#         for key, value in request.POST.items():
#             if key.startswith('check-'):
#                 carrito = CarroCompra.objects.get(id_carroCompra=value)
#                 carrito.pagado = True
#                 carrito.save()
#                 export_venta_to_excel(carrito)
#
#     return render(request, 'html/vista_Repartidor.html', context)


@login_required
def add_producto_carrito(request, pk):
    producto = Producto.objects.get(pk=pk)
    carritos = CarroCompra.objects.filter(usuario=request.user, enviado=False)
    if not carritos:
        carrito = CarroCompra.objects.create(usuario=request.user)
    else:
        carrito = carritos[0]

    carrito_item, creado = carrito.items.get_or_create(producto=producto)
    carrito_item.cantidad += 1
    carrito_item.save()

    if carrito_item:
        messages.success(request, f'Artículo "{producto.nombreP}" añadido al carrito.')

    return redirect('index')


@login_required
def add_oferta_carrito(request, pk):
    oferta = Oferta.objects.get(pk=pk)
    carritos = CarroCompra.objects.filter(usuario=request.user, enviado=False)
    if not carritos:
        carrito = CarroCompra.objects.create(usuario=request.user)
    else:
        carrito = carritos[0]

    carrito_item, creado = carrito.items.get_or_create(oferta=oferta)
    carrito_item.cantidad += 1
    carrito_item.save()

    if carrito_item:
        messages.success(request, f'Artículo "{oferta.nombreO}" añadido al carrito.')

    return redirect('index')


@login_required
def ajustar_carrito_item(request, pk, tipo):
    carrito_item = ArticuloCarro.objects.get(pk=pk)

    if tipo == "up":
        carrito_item.cantidad += 1
    elif tipo == "down":
        carrito_item.cantidad -= 1
    carrito_item.save()

    return redirect('index')


@login_required
def eliminar_carrito_item(request, pk):
    carrito_item = ArticuloCarro.objects.get(pk=pk)
    carrito_item.delete()

    return redirect('index')


@login_required
def pagar_carrito(request):
    carrito = CarroCompra.objects.filter(usuario=request.user, enviado=False)[0]
    carrito.pagado = True
    carrito.fecha_envio = datetime.now()
    carrito.save()
    if carrito.pagado:
        messages.success(request, 'En espera de confirmación del pago, puede demorar hasta 24h.')
    return redirect('index')


@login_required
def pedir_cuenta(request):
    suma = 0
    carritos = request.user.carritos.filter(enviado=True, pagado=False)
    for carrito in carritos:
        carrito.cerrado = True
        suma += carrito.precio_total()
        carrito.save()
    if carritos.last().cerrado:
        messages.success(request, f'Su pedido fue pagado con éxito.')
    return redirect('index')


@login_required
def crear_valoracion(request, pk):
    inmueble = get_object_or_404(Inmueble, pk=pk)

    if request.method == 'POST':
        valor = request.POST.get('valor')
        comentario = request.POST.get('comentario', '')

        if valor and valor.isdigit() and 1 <= int(valor) <= 5:
            Valoracion.objects.create(
                usuario=request.user,
                inmueble=inmueble,
                valor=int(valor),
                comentario=comentario
            )
            messages.success(request, "✅ Gracias por tu opinión.")
        else:
            messages.error(request, "❌ Selecciona una calificación válida.")

    return redirect('index')  # O a la lista si prefieres


@login_required
def editar_valoracion(request, pk):
    val = get_object_or_404(Valoracion, pk=pk, usuario=request.user)

    if request.method == 'POST':
        valor = request.POST.get('valor')
        comentario = request.POST.get('comentario', '')

        if valor and valor.isdigit() and 1 <= int(valor) <= 5:
            val.valor = int(valor)
            val.comentario = comentario
            val.save()
            messages.success(request, "✅ Valoración actualizada con éxito.")
        else:
            messages.error(request, "❌ Selecciona una calificación válida.")

    return redirect('producto:inmueble_detalle', pk=val.inmueble.pk if val.inmueble else val.producto.pk if val.producto else val.evento.pk if val.evento else val.oferta.pk)


@login_required
def eliminar_valoracion(request, pk):
    val = get_object_or_404(Valoracion, pk=pk, usuario=request.user)

    # Guardamos el objeto relacionado antes de eliminar
    inmueble_pk = val.inmueble.pk if val.inmueble else None
    producto_pk = val.producto.pk if val.producto else None
    evento_pk = val.evento.pk if val.evento else None
    oferta_pk = val.oferta.pk if val.oferta else None

    val.delete()
    messages.success(request, "🗑️ Valoración eliminada con éxito.")

    # Redirigir al detalle correspondiente
    if inmueble_pk:
        return redirect('producto:inmueble_detalle', pk=inmueble_pk)
    elif producto_pk:
        return redirect('producto:producto_detalle', pk=producto_pk)
    elif evento_pk:
        return redirect('producto:evento_detalle', pk=evento_pk)
    elif oferta_pk:
        return redirect('producto:oferta_detalle', pk=oferta_pk)
    else:
        return redirect('index')

