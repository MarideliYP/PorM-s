import os
from pathlib import Path
import dj_database_url
from django.urls import reverse_lazy

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# =============================================================================
# === SEGURIDAD Y ENTORNO ===
# =============================================================================

SECRET_KEY = os.getenv('SECRET_KEY')
if not SECRET_KEY:
    raise ValueError("La variable de entorno SECRET_KEY es obligatoria.")

DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'


ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', '*').split(',')

# =============================================================================
# === APLICACIONES ===
# =============================================================================

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "user",
    "producto",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "PrMas.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "django.template.context_processors.media",
            ],
        },
    },
]

WSGI_APPLICATION = "PrMas.wsgi.application"

AUTH_USER_MODEL = 'user.User'

# =============================================================================
# === BASE DE DATOS ===
# =============================================================================

# DATABASES = {
#     "default": {
#         "ENGINE": "django.db.backends.sqlite3",
#         "NAME": BASE_DIR / "db.sqlite3",
#     }
# }


DATABASES = {
    'default': dj_database_url.config(
        default=os.getenv('DATABASE_URL', 'sqlite:///db.sqlite3')
    )
}

# =============================================================================
# === CONTRASEÑAS ===
# =============================================================================

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator", "OPTIONS": {"min_length": 8}},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# =============================================================================
# === INTERNACIONALIZACIÓN ===
# =============================================================================

LANGUAGE_CODE = "es-es"
TIME_ZONE = "America/Havana"
USE_I18N = True
USE_TZ = True

# =============================================================================
# === ARCHIVOS ESTÁTICOS Y DE MEDIOS ===
# =============================================================================

STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# =============================================================================
# === LOGIN / REDIRECCIONES ===
# =============================================================================

LOGIN_URL = reverse_lazy('user:login')
LOGIN_REDIRECT_URL = reverse_lazy('index')
LOGOUT_REDIRECT_URL = reverse_lazy('index')

# =============================================================================
# === CORREO ===
# =============================================================================

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER', 'myaburperez@gmail.com')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD', 'bzph xsms wzix gviy')

# =============================================================================
# === SEGURIDAD EN PRODUCCIÓN ===
# =============================================================================

if not DEBUG:
    SECURE_SSL_REDIRECT = True
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    SECURE_HSTS_SECONDS = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    SECURE_BROWSER_XSS_FILTER = True
    X_FRAME_OPTIONS = "DENY"
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_REFERRER_POLICY = "strict-origin-when-cross-origin"

# =============================================================================
# === ERRORES Y ADMINISTRADORES ===
# =============================================================================

ADMINS = [("Marideli", os.getenv('ADMIN_EMAIL', 'myaburperez@gmail.com'))]
MANAGERS = ADMINS
SERVER_EMAIL = os.getenv('SERVER_EMAIL', 'error@pormas.com')

# =============================================================================
# === LÍMITES DE SEGURIDAD ===
# =============================================================================

DATA_UPLOAD_MAX_MEMORY_SIZE = 5242880      # 5 MB
FILE_UPLOAD_MAX_MEMORY_SIZE = 5242880      # 5 MB
DATA_UPLOAD_MAX_NUMBER_FIELDS = 1000

# =============================================================================
# === OTROS ===
# =============================================================================

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


