from django.core.exceptions import ValidationError


def email_validator(value):
    if not value.split('.')[-1].isalpha():
        raise ValidationError("No se permiten números como parte del dominio.")
    if len(value.split('.')[-1]) < 2:
        raise ValidationError("Dirección de correo inválida")


def not_empty(value):
    if value == '' or value is None:
        raise ValidationError("Por favor llene este campo")
