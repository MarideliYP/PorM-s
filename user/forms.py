from django import forms
from .models import User
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.password_validation import validate_password
from django.core.validators import EmailValidator
from .custom_validators import email_validator, not_empty
from django.contrib.auth.models import Group


class User_form(forms.ModelForm):
    image = forms.ImageField(
        widget=forms.FileInput(
            attrs={
                'class': 'form-control mb-3',
                'placeholder': 'Foto de perfil',
            }
        ),
        label='Foto de perfil',
    )

    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'name': 'username',
                'class': 'form-control mb-3',
                'placeholder': 'Usuario',

            }
        ),
        label="Usuario",
        max_length=12,
        validators=[not_empty]
    )

    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                'class': 'form-control mb-3',
                'placeholder': 'ejemplo@email.com',
            }
        ),
        label='Email',
        validators=[EmailValidator(), email_validator]
    )

    first_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control mb-3 not-numeric',
                'placeholder': 'Nombre',
            }
        ),
        label='Nombre',
        max_length=30,

    )

    last_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control mb-3 not-numeric',
                'placeholder': 'Apellidos',
            }
        ),
        label='Apellidos',
        max_length=30,
    )

    dir = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'name': 'dir',
                'class': 'form-control mb-3',
                'placeholder': 'Provincia, Municipio, calle/calles no.',

            }
        ),
        label="Dirección",
        validators=[not_empty]
    )

    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'name': 'password',
                'id': 'password',
                'class': 'form-control mb-3',
                'placeholder': 'Contraseña',
            }
        ),
        label='Contraseña',
        validators=[validate_password],
    )

    check_pass = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'id': 'check_pass',
                'class': 'form-control mb-3',
                'placeholder': 'Repita su contraseña',
            }
        ),
        label="Repita su contraseña"
    )

    class Meta:
        model = User
        fields = [
            'image',
            'username',
            'email',
            'first_name',
            'last_name',
            'dir',
            'password',
            'check_pass',
        ]

    def __init__(self, *args, **kwargs):
        self.pk = kwargs.pop('pk', None)
        super(User_form, self).__init__(*args, **kwargs)
        self.fields['first_name'].required = False  # hacer que campos no sean requeridos
        self.fields['last_name'].required = False
        for field in self.fields.values():
            field.error_messages = {
                'required': 'Por favor llene este campo'}

    def clean(self):  # validaciones que dependen de mas de un campo
        cleaned_data = super().clean()  # obtiene un diccionario con todos los campos limpios
        password = cleaned_data.get("password")
        check_pass = cleaned_data.get("check_pass")

        if password != check_pass:  # revisa que las passes sean iwales ez :v
            self.add_error('password', "Las contraseñas no coinciden")

    def clean_username(self):  # validaciones para un campo en especifico
        cleaned_data = super().clean()
        username = cleaned_data.get("username")

        if User.objects.filter(username=username).exists():  # revisa que no exista ya un username igual que el actual
            user = User.objects.get(username=username)
            if self.pk != user.pk:
                self.add_error('username',
                               "Ese nombre de usuario no está disponible")

        return username

    def clean_email(self):
        cleaned_data = super().clean()
        email = cleaned_data.get("email")

        if not email:
            return email  # Ya se manejará el error de "required" automáticamente

        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            # Si es edición, permitir el mismo email
            if self.instance and self.instance.pk == user.pk:
                return email
            self.add_error('email', "Ya existe un usuario con este correo electrónico.")

        return email

    def save(self, commit=True):
        is_new = not self.instance.pk
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])

        if commit:
            user.save()
            if is_new:
                group = Group.objects.get(name="Cliente")
                group.user_set.add(user)
        return user


class VerificationCodeForm(forms.Form):
    code = forms.CharField(
        max_length=5,
        widget=forms.TextInput(attrs={'placeholder': 'Código de 5 dígitos', 'class': 'form-control'})
    )


class Login_form(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'name': 'username',
                'class': 'form-control mb-3',
                'placeholder': 'Usuario',
            }
        ),
        label="Usuario",
        max_length=12
    )

    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'name': 'password',
                'id': 'password',
                'class': 'form-control mb-3',
                'placeholder': 'Contraseña',
            }
        ),
        label='Contraseña',
    )

    error_messages = {
        'invalid_login': "Credenciales incorrectas. Por favor, verifica tus datos.",
        'inactive': "Esta cuenta no esta activa",
    }

    class Meta:
        model = User
        fields = [
            'username',
            'password',
        ]

    def __init__(self, *args, **kwargs):
        self.pk = kwargs.pop('pk', None)
        super(Login_form, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.error_messages = {
                'required': 'Por favor llene este campo'}


