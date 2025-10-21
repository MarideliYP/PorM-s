import os
from django.utils import timezone
import datetime
from django.contrib import auth
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from producto.forms import Reserva_form
from producto.models import Reserva, ContratoFirmado, CarroCompra
from .models import User
from django.utils.decorators import method_decorator
from django.http import HttpResponseRedirect
from django.urls import reverse
from .forms import User_form, Login_form
from django.contrib.auth.views import LoginView
from django.contrib.auth.models import Group
from django.core.mail import send_mail
import random
from django.conf import settings
from django.contrib import messages
from .forms import VerificationCodeForm
from django.views.generic import (
    CreateView,
    ListView,
    DetailView,
)


class Login(LoginView):
    template_name = 'user/login.html'
    authentication_form = Login_form

    def form_valid(self, form):
        login(self.request, form.get_user())
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        user = self.request.user
        if user.groups.filter(name='Empresa').exists():
            return reverse('vistaempresa')
        else:
            return reverse('index')


class Register(CreateView):
    template_name = 'user/register.html'
    form_class = User_form

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        # Ocultar el campo 'grupo' si el usuario no es admin
        if not (self.request.user.is_authenticated and self.request.user.is_staff):
            form.fields.pop('grupo', None)
        return form

    def form_valid(self, form):
        email = form.cleaned_data.get('email')
        es_admin = self.request.user.is_authenticated and self.request.user.is_staff

        # === FLUJO PARA USUARIOS NORMALES: verificar si el correo ya existe ===
        if not es_admin and User.objects.filter(email=email).exists():
            existing_user = User.objects.get(email=email)

            # Si el usuario ya logueado es el dueño del correo, redirigir
            if self.request.user.is_authenticated and self.request.user == existing_user:
                login(self.request, existing_user)
                return redirect('PrMas:vistaempresa' if existing_user.groups.filter(name="Empresa").exists()
                                else 'PrMas:index')

            # Enviar aviso al dueño del correo
            subject = 'Alguien intentó usar tu correo'
            message = f'Se intentó registrar un nuevo usuario con tu correo {email}. Si no fuiste tú, ten cuidado.'
            send_mail(subject, message, settings.EMAIL_HOST_USER, [existing_user.email], fail_silently=True)

            form.add_error('email', 'Ya existe un usuario con este correo electrónico.')
            return self.form_invalid(form)

        # === FLUJO PARA ADMIN: crear usuario directamente ===
        if es_admin:
            user = form.save(commit=False)
            user.is_verified = True  # Verificado automáticamente
            user.verification_code = None
            user.code_expiration = None
            user.save()

            # Asignar grupo si se seleccionó
            grupo = form.cleaned_data.get('grupo')
            if grupo:
                user.groups.add(grupo)

                # Si el grupo es "Administrador", dar permisos especiales
                if grupo.name == "Administrador":
                    user.is_staff = True
                    user.is_superuser = True
                    user.save()

            messages.success(self.request, f'✅ Usuario "{user.username}" creado exitosamente.')
            return redirect('user:list')  # Cambia por tu URL de lista

        # === FLUJO PARA USUARIO NORMAL: registro con verificación ===
        user = form.save(commit=False)
        user.is_verified = False
        code = generate_verification_code()
        user.verification_code = code
        user.code_expiration = timezone.now() + datetime.timedelta(minutes=10)
        user.save()

        # Enviar código de verificación
        subject = 'Código de verificación'
        message = f'Tu código de verificación es: {code}'
        send_mail(subject, message, settings.EMAIL_HOST_USER, [user.email], fail_silently=False)

        messages.info(self.request, 'Revisa tu correo para verificar tu cuenta.')
        return redirect('user:verify_email', username=user.username)

    def form_invalid(self, form):
        return render(self.request, self.template_name, {
            'form': form,
        })


def generate_verification_code():
    return str(random.randint(10000, 99999))


def verify_email_view(request, username):
    user = User.objects.get(username=username)

    now = timezone.now()
    if user.code_blocked_until and now < user.code_blocked_until:
        minutes_left = (user.code_blocked_until - now).seconds // 60
        messages.warning(request, f'Demasiros intentos fallidos. Inténtalo nuevamente en {minutes_left} minutos.')
        return render(request, 'user/verify_email.html')

    if request.method == 'POST':
        form = VerificationCodeForm(request.POST)
        if form.is_valid():
            entered_code = form.cleaned_data['code']

            if user.is_code_valid(entered_code):
                user.is_verified = True
                user.verification_code = None
                user.failed_attempts = 0
                user.code_blocked_until = None
                user.save()
                messages.success(request, '✅ ¡Correo verificado exitosamente!')
                return redirect('user:login')
            else:
                user.failed_attempts += 1
                if user.failed_attempts >= 5:
                    user.code_blocked_until = now + datetime.timedelta(minutes=15)
                    messages.error(request, '❌ Demasiados intentos. Bloqueado por 15 minutos.')
                else:
                    messages.error(request, f'❌ Código incorrecto. Te quedan {5 - user.failed_attempts} intentos.')
                user.save()

    else:
        form = VerificationCodeForm()

    context = {
        'username': username,
        'form': form,
        'blocked': user.code_blocked_until and now < user.code_blocked_until,
        'resend_allowed': not user.code_blocked_until or now > user.code_blocked_until
    }
    return render(request, 'user/verify_email.html', context)


def resend_code_view(request, username):
    user = User.objects.get(username=username)
    now = timezone.now()

    if user.code_blocked_until and now < user.code_blocked_until:
        messages.warning(request, 'Aún estás bloqueado por demasiados intentos.')
        return redirect('user:verify_email', username=username)

    code = generate_verification_code()
    user.verification_code = code
    user.code_expiration = now + datetime.timedelta(minutes=10)
    user.failed_attempts = 0
    user.save()

    subject = 'Nuevo código de verificación'
    message = f'Tu nuevo código es: {code}'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [user.email]
    send_mail(subject, message, email_from, recipient_list)

    messages.success(request, '📧 Nuevo código enviado.')
    return redirect('user:verify_email', username=username)


def logout_view(request):
    auth.logout(request)

    return redirect('/')


@method_decorator(login_required, name='dispatch')
class User_details(DetailView):
    model = User
    template_name = 'user/user_details.html'
    context_object_name = 'usuario'  # Nombre con el que accederás en el template

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        usuario = self.get_object()

        context['reservas'] = Reserva.objects.filter(usuario=usuario).select_related('evento')
        context['contratos'] = ContratoFirmado.objects.filter(usuario=usuario)
        context['reserva_forms'] = [
            (reserva, Reserva_form(instance=reserva)) for reserva in context['reservas']
        ]
        return context


@login_required
def user_delete(request, pk):
    user = User.objects.get(pk=pk)
    user.delete()

    return redirect('user:list')


@method_decorator(login_required, name='dispatch')
class User_list(ListView):
    model = User
    template_name = 'user/user_list.html'
    context_object_name = 'object_list'

    def get_queryset(self):
        return User.objects.all().prefetch_related('carritos')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Añadir carritos con pago (con imagen en `pagar`)
        context['carritos_con_pago'] = CarroCompra.objects.filter(
            pagar__isnull=False,
            pagado=False  # Solo los que aún no están marcados como pagados
        ).select_related('usuario').prefetch_related('items')
        return context


@login_required
def user_update(request, pk):
    user = User.objects.get(pk=pk)

    # Si el usuario que se está editando es el mismo que está logueado
    if request.user.pk == user.pk:
        editing_self = True
    else:
        editing_self = False

    if request.method == 'POST':
        form = User_form(request.POST, instance=user, pk=pk)
        group = Group.objects.get(name=request.POST['roles'])

        if form.is_valid():
            user.is_staff = False
            user.is_superuser = False
            user.groups.clear()
            user.groups.add(group)

            if group.name == 'Administrador':
                user.is_staff = True
                user.is_superuser = True

            # Si estoy editando mi propia cuenta, asegurarme que no pierdo acceso
            if editing_self:
                user.is_staff = True
                user.is_superuser = True
                user.groups.add(Group.objects.get(name='Administrador'))

            form.save()
            return redirect('user:list')

    else:
        form = User_form(instance=user, pk=pk)

    context = {'form': form}
    return render(request, 'user/user_update.html', context)


@login_required
def update_img(request, pk):
    # 1. Validar que el usuario solo pueda cambiar su propia foto (o es admin)
    if request.user.pk != pk and not request.user.is_staff:
        messages.error(request, "No tienes permiso para hacer esto.")
        return redirect("user:details", pk=request.user.pk)

    user = User.objects.get(pk=pk)

    if request.method == 'POST':
        # 2. Verificar si se subió un archivo
        if 'image' in request.FILES:
            new_image = request.FILES['image']

            # 3. Validar extensión (solo .jpg, .jpeg, .png)
            allowed_extensions = ['.jpg', '.jpeg', '.png']
            ext = os.path.splitext(new_image.name)[1].lower()

            if ext not in allowed_extensions:
                messages.error(request, "❌ Solo se permiten archivos .jpg y .png.")
                return redirect("user:details", pk=pk)

            # 4. Opcional: eliminar la imagen anterior (si no es la por defecto)
            if user.image and user.image.name != 'img/user.png':
                if os.path.isfile(user.image.path):
                    os.remove(user.image.path)

            # 5. Asignar y guardar
            user.image = new_image
            user.save()
            messages.success(request, "✅ Foto actualizada con éxito.")
        else:
            messages.warning(request, "⚠️ No seleccionaste ninguna imagen.")

    return redirect("user:details", pk=pk)
