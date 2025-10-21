from .models import Producto, Inmueble, Oferta, Evento, Reserva, Media, Empresa
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
            ('turismo', 'Turismo'),
            ('comidas-bebidas', 'Comidas y bebidas'),
            ('articulo-hogar', 'Articulos del hogar'),
            ('belleza', 'Belleza'),
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


class Inmueble_form(forms.ModelForm):
    nombreI = forms.CharField(
        max_length=220,
        label='Nombre del Inmueble',
        widget=forms.TextInput(attrs={'class': 'form-control mb-3'})
    )

    detalles = forms.CharField(
        max_length=1000,
        label='Detalles del Inmueble',
        widget=forms.TextInput(attrs={'class': 'form-control mb-3'})
    )

    image = forms.ImageField(
        label='Imagen del Inmueble',
        widget=forms.FileInput(attrs={'class': 'form-control mb-3'})
    )

    numagente = forms.IntegerField(
        label='Número de teléfono del agente inmobiliario',
        widget=forms.NumberInput(attrs={
            'class': 'form-control mb-3',
            'placeholder': 'Ej: +5351234567'
        })
    )

    precio = forms.IntegerField(
        label='Precio del Inmueble',
        widget=forms.NumberInput(attrs={'class': 'form-control mb-3 '})
    )

    tipo = forms.ChoiceField(
        choices=[
            (None, 'Seleccione el municipio del inmueble'),
            ('arroyo_naranjo', 'Arroyo Naranjo'),
            ('boyeros', 'Boyeros'),
            ('cerro', 'Cerro'),
            ('cotorro', 'Cotorro'),
            ('diez_de_octubre', 'Diez de Octubre'),
            ('guanabacoa', 'Guanabacoa'),
            ('habana_del_este', 'La Habana del Este'),
            ('habana_vieja', 'La Habana Vieja'),
            ('la Lisa', 'La Lisa'),
            ('marianao', 'Marianao'),
            ('playa', 'Playa'),
            ('plaza', 'Plaza de la Revolución'),
            ('regla', 'Regla'),
            ('san_miguel_del_padron', 'San Miguel del Padrón'),
        ],

        widget=forms.Select(attrs={'class': 'form-control form-select bg-transparent border-0 '
                                            'border-bottom rounded-0 border-light-subtle text-primary'})
    )

    class Meta:
        model = Inmueble
        fields = [
            'nombreI',
            'detalles',
            'image',
            'numagente',
            'precio',
            'tipo',
        ]

    def __init__(self, *args, **kwargs):
        super(Inmueble_form, self).__init__(*args, **kwargs)
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

    fechahora = forms.DateTimeField(
        label='Fecha y hora',
        widget=forms.DateTimeInput(
            attrs={
                'class': 'form-control mb-3',
                'type': 'datetime-local'
            },
            format='%Y-%m-%dT%H:%M'
        ),
        input_formats=['%Y-%m-%dT%H:%M']
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
            'fechahora',
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
        max_value=10,
        min_value=1,
        label='Cantidad de Personas',
        widget=forms.NumberInput(attrs={
            'class': 'form-control mb-3',
            'placeholder': 'Cantidad de personas (máx. 10)'
        })
    )

    num_confirm = forms.IntegerField(
        label='Número de teléfono para confirmar',
        widget=forms.NumberInput(attrs={
            'class': 'form-control mb-3',
            'placeholder': 'Ej: 51234567'
        })
    )

    mensaje = forms.CharField(
        max_length=1000,
        required=False,
        label='Comentario o sugerencia (opcional)',
        widget=forms.Textarea(attrs={
            'class': 'form-control mb-3',
            'rows': 3,
            'placeholder': 'Algún comentario o petición especial...'
        })
    )

    estado = forms.BooleanField(
        label='Confirmada',
        required=False,
        initial=False,
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input ms-2',
            'style': 'margin-left: 0; transform: scale(1.3);'
        })
    )

    class Meta:
        model = Reserva
        fields = [
            'num_personas',
            'num_confirm',
            'mensaje',
            'estado',
        ]

    def __init__(self, *args, **kwargs):
        super(Reserva_form, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.error_messages = {
                'required': 'Por favor llene este campo',
                'max_length': 'Asegúrese que este valor tenga cuando más %(limit_value)d caracteres (tiene %('
                              'show_value)d).',
            }


class Empresa_form(forms.ModelForm):
    nombre = forms.CharField(
        max_length=120,
        label='Nombre de la Empresa',
        widget=forms.TextInput(attrs={'class': 'form-control mb-3'})
    )

    description = forms.CharField(
        max_length=120,
        label='Detalles de la Empresa',
        widget=forms.TextInput(attrs={'class': 'form-control mb-3'})
    )

    image = forms.ImageField(
        label='Imagen de la Empresa',
        widget=forms.FileInput(attrs={'class': 'form-control mb-3'})
    )

    class Meta:
        model = Empresa
        fields = ['nombre', 'description', 'image']

    def __init__(self, *args, **kwargs):
        super(Empresa_form, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.error_messages = {
                'required': 'Por favor llene este campo',
                'max_length': 'Asegúrese que este valor tenga cuando más %(limit_value)d caracteres (tiene %('
                              'show_value)d).',
            }


class MediaForm(forms.ModelForm):

    archivo = forms.FileField(
        label='Imagen/Video',
        widget=forms.FileInput(attrs={'class': 'form-control mb-3'})
    )

    orden = forms.IntegerField(
        label='# de archivo',
        max_value=10,
        widget=forms.NumberInput(attrs={'class': 'form-control mb-3'})
    )

    tipo = forms.ChoiceField(
        choices=[
            (None, 'Seleccione el tipo de archivo'),
            ('imagen', 'Imagen'),
            ('video', 'Video'),
        ],
        widget=forms.Select(attrs={'class': 'form-control form-select bg-transparent border-0 '
                                            'border-bottom rounded-0 border-light-subtle text-primary'})
    )

    class Meta:
        model = Media
        fields = ['archivo', 'orden', 'tipo']

    def clean_archivo(self):
        archivo = self.cleaned_data.get('archivo')
        if not archivo:
            raise forms.ValidationError("Este campo es obligatorio.")

        ext = archivo.name.lower().split('.')[-1]
        tipo = self.cleaned_data.get('tipo')

        if tipo == 'imagen' and ext not in ['jpg', 'jpeg', 'png', 'gif']:
            raise forms.ValidationError("Las imágenes deben ser JPG, PNG o GIF.")
        if tipo == 'video' and ext not in ['mp4', 'mov', 'webm', 'avi']:
            raise forms.ValidationError("Los videos deben ser MP4, MOV, AVI o WEBM.")
        return archivo
