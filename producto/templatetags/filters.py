from django import template

register = template.Library()


@register.filter
def avg_rating(valoraciones):
    try:
        if not valoraciones or not valoraciones.exists():
            return 0
        return round(sum(v.valor for v in valoraciones) / valoraciones.count(), 1)
    except (ZeroDivisionError, AttributeError):
        return 0


@register.filter
def stars_info(valoraciones):
    if not valoraciones or not valoraciones.exists():
        return {'full': 0, 'half': 0, 'empty': 5}

    avg = sum(v.valor for v in valoraciones) / valoraciones.count()
    full = int(avg)
    half = 1 if 0.25 <= avg - full <= 0.75 else 0
    empty = 5 - full - half

    return {'full': full, 'half': half, 'empty': empty}


# Tipos de productos
TIPOS_PRODUCTOS = (
    ('turismo', 'Turismo'),
    ('comidas-bebidas', 'Comidas y bebidas'),
    ('articulo-hogar', 'Articulos del hogar'),
    ('belleza', 'Belleza'),
)

# Tipos de inmuebles (municipios)
TIPOS_INMUEBLES = (
    ('arroyo_naranjo', 'Arroyo Naranjo'),
    ('boyeros', 'Boyeros'),
    ('cerro', 'Cerro'),
    ('cotorro', 'Cotorro'),
    ('diez_de_octubre', 'Diez de Octubre'),
    ('guanabacoa', 'Guanabacoa'),
    ('habana_del_este', 'La Habana del Este'),
    ('habana_vieja', 'La Habana Vieja'),
    ('marianao', 'Marianao'),
    ('playa', 'Playa'),
    ('plaza', 'Plaza de la Revolución'),
    ('regla', 'Regla'),
    ('san_miguel_del_padron', 'San Miguel del Padrón'),
)

# Diccionarios para búsquedas rápidas
PRODUCTO_TIPO_MAP = {key: f"filter-{key}" for key, label in TIPOS_PRODUCTOS}
INMUEBLE_TIPO_MAP = {key: f"filter-{key}" for key, label in TIPOS_INMUEBLES}


@register.filter
def get_filter_class(obj):
    tipo = getattr(obj, 'tipo', None)
    if not tipo:
        return ""

    # Normalizar: a minúsculas, reemplazar _ por -
    tipo_clean = tipo.strip().lower().replace('_', '-')

    if tipo_clean in PRODUCTO_TIPO_MAP:
        return PRODUCTO_TIPO_MAP[tipo_clean]
    elif tipo_clean in INMUEBLE_TIPO_MAP:
        return INMUEBLE_TIPO_MAP[tipo_clean]
    else:
        return ""
