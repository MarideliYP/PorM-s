from django.utils import timezone
import datetime
from django.contrib import auth
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from .models import User
from django.utils.decorators import method_decorator
from django.http import HttpResponseRedirect, HttpResponse
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
    UpdateView,
    DetailView,
)


class Login(LoginView):
    template_name = 'user/login.html'
    authentication_form = Login_form

    def form_valid(self, form):
        login(self.request, form.get_user())
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        if User.groups.filter(name="Empresa").exists():
            return redirect('PorMás:vistaempresa')
        else:
            return redirect('PorMás:index')


class Register(CreateView):
    template_name = 'user/register.html'
    form_class = User_form

    def form_valid(self, form):
        email = form.cleaned_data.get('email')

        # Si ya existe un usuario con ese correo
        if User.objects.filter(email=email).exists():
            existing_user = User.objects.get(email=email)

            # Si el usuario actual está logueado y es el mismo dueño del correo
            if self.request.user.is_authenticated and self.request.user == existing_user:
                # Autenticar y redirigir directamente
                login(self.request, existing_user)
                return redirect('PorMás:vistaempresa' if existing_user.groups.filter(name="Empresa").exists() else 'PorMás:index')

            # Si NO está logueado o no es el dueño, enviar aviso al dueño
            subject = 'Alguien intentó usar tu correo'
            message = f'Un intento de registro fue realizado con tu correo {email}. Si no fuiste tú, por favor toma medidas.'
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [existing_user.email]

            send_mail(subject, message, email_from, recipient_list, fail_silently=True)

            # Mostrar error en el formulario
            form.add_error('email', 'Ya existe un usuario con este correo electrónico.')
            return self.form_invalid(form)

        # Si el correo es nuevo, registrar normalmente
        user = form.save(commit=False)
        user.is_verified = False
        code = generate_verification_code()
        user.verification_code = code
        user.code_expiration = timezone.now() + datetime.timedelta(minutes=10)
        user.save()

        # Enviar código de verificación
        subject = 'Código de verificación'
        message = f'Tu código de verificación es: {code}'
        recipient_list = [user.email]
        send_mail(subject, message, settings.EMAIL_HOST_USER, recipient_list, fail_silently=False)

        return redirect('verify_email', username=user.username)

    def form_invalid(self, form):
        return render(self.request, self.template_name, {
            'form': form,
            'email_already_exists': True
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
                return redirect('login')
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
        return redirect('verify_email', username=username)

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
    return redirect('verify_email', username=username)


def logout_view(request):
    auth.logout(request)

    return redirect('/')


@method_decorator(login_required, name='dispatch')
class User_details(DetailView):
    queryset = User.objects.all()
    template_name = 'user/user_details.html'


@login_required
def user_delete(request, pk):
    user = User.objects.get(pk=pk)
    user.delete()

    return redirect('user:list')


@method_decorator(login_required, name='dispatch')
class User_list(ListView):
    queryset = User.objects.all()
    template_name = 'user/user_list.html'


@method_decorator(login_required, name='dispatch')
class User_update(UpdateView):
    queryset = User.objects.all()
    template_name = 'user/user_update.html'
    form_class = User_form

    def get_success_url(self):
        return reverse('user:list')


@login_required
def user_update(request, pk):
    user = User.objects.get(pk=pk)
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

            form.save()
            return redirect('user:list')

    else:
        form = User_form(instance=User.objects.get(pk=pk), pk=pk)

    context = {'form': form}

    return render(request, 'user/user_update.html', context)
