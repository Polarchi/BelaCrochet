"""
Django settings for bela_crochet project.

Generated for the Bela Crochet e-commerce MVP.  
Usa SQLite por defecto y tiene configuraciones básicas 
para Ecuador. Ver README para más opciones.
"""
from pathlib import Path
import os

# Build paths inside the project
BASE_DIR = Path(__file__).resolve().parent.parent

# =======================
# Seguridad
# =======================
SECRET_KEY = os.environ.get(
    "DJANGO_SECRET_KEY",
    "django-insecure-change-me"  # ⚠️ solo para desarrollo
)

DEBUG = True
ALLOWED_HOSTS = ["*"]  # en producción cambia esto por tu dominio

# =======================
# Aplicaciones
# =======================
INSTALLED_APPS = [
    # Django core apps
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",

    # Third-party apps
    "django_filters",

    # Local apps
    "core",
    "accounts",
    "catalog",
    "cart",
    "checkout",
    "orders",
    "receipts",
    "pages",
]

SITE_ID = 1

# =======================
# Middleware
# =======================
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "bela_crochet.urls"

# =======================
# Templates
# =======================
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                # custom context processors
                "core.context_processors.site_settings",
                "core.context_processors.cart_mini",
            ],
        },
    },
]

WSGI_APPLICATION = "bela_crochet.wsgi.application"

# =======================
# Base de datos
# =======================
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# =======================
# Validación de contraseñas
# =======================
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# =======================
# Internacionalización
# =======================
LANGUAGE_CODE = "es-ec"
TIME_ZONE = "America/Guayaquil"
USE_I18N = True
USE_TZ = True

# =======================
# Archivos estáticos y media
# =======================
STATIC_URL = "static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"

MEDIA_URL = "media/"
MEDIA_ROOT = BASE_DIR / "media"

# =======================
# Configuración adicional
# =======================
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Email backend
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
# Para usar Gmail u otro, luego lo cambias aquí ↑

# Carrito
CART_SESSION_ID = "cart_id"

# PDF (desactivado por defecto)
ENABLE_PDF = False

# Redirecciones de login/logout
LOGIN_REDIRECT_URL = "/"   # después de iniciar sesión va al inicio
LOGOUT_REDIRECT_URL = "/"  # después de cerrar sesión va al inicio
