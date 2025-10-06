import os
from pathlib import Path
import dj_database_url
from django.urls import reverse_lazy
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
# =============================================================================
# === SEGURIDAD Y ENTORNO ===
# =============================================================================
# CAMBIO: Reemplazado config() con os.getenv(). Configura SECRET_KEY en Railway como secreto.
SECRET_KEY = os.getenv('SECRET_KEY', 'django-insecure-default-key-for-local-dev-only-do-not-use-in-prod')
# CAMBIO: Reemplazado config() con os.getenv(). Usa 'False' en Railway para producción.
DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'
# CAMBIO: Reemplazado config() con os.getenv(). Para Railway, configura como 'tu-app.railway.app,127.0.0.1,localhost'.
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', '.railway.app').split(',')
# =============================================================================
# === APLICACIONES ===
# =============================================================================
# CAMBIO: Reemplazado config() con os.getenv(). Para Railway, configura como 'tu-app.railway.app,127.0.0.1,localhost'.
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', '.railway.app').split(',')
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
