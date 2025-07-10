from .models import Producto, Oferta, Evento, Reserva
from django import forms


class Producto_form(forms.ModelForm):
    nombreP = forms.CharField(
        max_length=120,
        label='Nombre del Producto',
        widget=forms.TextInput(attrs={'class': 'form-control mb-3'})
    )

    detalles = forms.CharField(
        max_length=120,
        label='Detalles del Producto',
        widget=forms.TextInput(attrs={'class': 'form-control mb-3'})
    )

    image = forms.ImageField(
        label='Imagen del Producto',
        widget=forms.FileInput(attrs={'class': 'form-control mb-3'})
    )

    precio = forms.IntegerField(
        label='Precio del Producto',
        widget=forms.NumberInput(attrs={'class': 'form-control mb-3 '})
    )

    tipo = forms.ChoiceField(
        choices=[
            (None, 'Seleccione el tipo de producto'),
            ('perfumes', 'Perfumes'),
            ('bebidas', 'Bebidas'),
            ('articulo-hogar', 'Articulos del hogar'),
            ('inmuebles', 'Inmuebles'),
        ],

        widget=forms.Select(attrs={'class': 'form-control form-select bg-transparent border-0 '
                                            'border-bottom rounded-0 border-light-subtle text-primary'})
    )

    class Meta:
        model = Producto
        fields = [
            'nombreP',
            'detalles',
            'image',
            'precio',
            'tipo',
        ]

    def __init__(self, *args, **kwargs):
        super(Producto_form, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.error_messages = {
                'required': 'Por favor llene este campo',
                'invalid_image': 'Imagen no válida',
                'max_length': 'Asegúrese que este valor tenga cuando más %(limit_value)d caracteres (tiene %('
                              'show_value)d).',
            }


class Oferta_form(forms.ModelForm):
    nombreO = forms.CharField(
        max_length=120,
        label='Nombre de la Oferta',
        widget=forms.TextInput(attrs={'class': 'form-control mb-3'})
    )

    description = forms.CharField(
        max_length=120,
        label='Descripción de la Oferta',
        widget=forms.TextInput(attrs={'class': 'form-control mb-3'})
    )

    image = forms.ImageField(
        label='Imagen de la Oferta',
        widget=forms.FileInput(attrs={'class': 'form-control mb-3'})
    )

    precio = forms.IntegerField(
        label='Precio de la Ofreta',
        widget=forms.NumberInput(attrs={'class': 'form-control mb-3'})
    )

    tipo = forms.ChoiceField(
        choices=[
            (None, 'Seleccione el tipo de oferta'),
            ('marketimg', 'Marketing Digital'),
            ('promocion', 'Promoción y Publicidad'),
            ('carteles', 'Diseño de Carteles y Fotos'),
            ('gestion', 'Gestión de Compra y Venta Inmobiliaria')
        ],
        widget=forms.Select(attrs={'class': 'form-control form-select bg-transparent border-0 '
                                            'border-bottom rounded-0 border-light-subtle text-primary'})
    )

    class Meta:
        model = Oferta
        fields = [
            'nombreO',
            'description',
            'image',
            'precio'
        ]

    def __init__(self, *args, **kwargs):
        super(Oferta_form, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.error_messages = {
                'required': 'Por favor llene este campo',
                'invalid_image': 'Imagen no válida',
                'max_length': 'Asegúrese que este valor tenga cuando más %(limit_value)d caracteres (tiene %('
                              'show_value)d).',
            }


class Evento_form(forms.ModelForm):
    nombreE = forms.CharField(
        max_length=30,
        label='Nombre del Evento',
        widget=forms.TextInput(attrs={'class': 'form-control mb-3'})
    )

    description = forms.CharField(
        max_length=120,
        label='Descripción del Evento',
        widget=forms.TextInput(attrs={'class': 'form-control mb-3'})
    )

    image = forms.ImageField(
        label='Imagen del Evento',
        widget=forms.FileInput(attrs={'class': 'form-control mb-3'})
    )

    preciocover = forms.FloatField(
        label='Precio del Cover',
        widget=forms.NumberInput(attrs={'class': 'form-control mb-3'})
    )

    capacidad = forms.IntegerField(
        label='Entradas disponibles',
        widget=forms.NumberInput(attrs={'class': 'form-control mb-3'})
    )

    class Meta:
        model = Evento
        fields = [
            'nombreE',
            'description',
            'image',
            'preciocover',
            'capacidad'
        ]

    def __init__(self, *args, **kwargs):
        super(Evento_form, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.error_messages = {
                'required': 'Por favor llene este campo',
                'invalid_image': 'Imagen no válida',
                'max_length': 'Asegúrese que este valor tenga cuando más %(limit_value)d caracteres (tiene %('
                              'show_value)d).',
            }


class Reserva_form(forms.ModelForm):
    num_personas = forms.IntegerField(
        max_value=500,
        label='Cantidad de Personas',
        widget=forms.NumberInput(attrs={'class': 'form-control mb-3'})
    )

    num_confirm = forms.IntegerField(
        label='Número de teléfono a confirmar',
        widget=forms.NumberInput(attrs={'class': 'form-control mb-3'})
    )

    mensaje = forms.CharField(
        max_length=30,
        required=False,
        label='Comentario o sugerencia (opcional)',
        widget=forms.TextInput(attrs={'class': 'form-control mb-3'})
    )

    class Meta:
        model = Reserva
        fields = [
            'num_personas',
            'num_confirm',
            'mensaje',
        ]

    def __init__(self, *args, **kwargs):
        super(Reserva_form, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.error_messages = {
                'required': 'Por favor llene este campo',
                'max_length': 'Asegúrese que este valor tenga cuando más %(limit_value)d caracteres (tiene %('
                              'show_value)d).',
            }
