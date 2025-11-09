"""
Django settings for alx_backend_security project.
"""

from pathlib import Path
import os
import environ

# ---------------------------------------------------------------------
# Environment Setup
# ---------------------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent

# Initialize environment variables
env = environ.Env(
    DEBUG=(bool, False)
)

# Read .env file
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

# ---------------------------------------------------------------------
# Basic Settings
# ---------------------------------------------------------------------
SECRET_KEY = env('SECRET_KEY')
DEBUG = env('DEBUG')
ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', default=['127.0.0.1', 'localhost'])

# ---------------------------------------------------------------------
# Application Definition
# ---------------------------------------------------------------------
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Third-party apps
    'rest_framework',
    'drf_yasg',  # Swagger API documentation

    # Custom app
    'ip_tracking',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',

    # IP Tracking Middleware (must come before CSRF)
    'ip_tracking.middleware.IPTrackingMiddleware',

    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'alx_backend_security.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'alx_backend_security.wsgi.application'

# ---------------------------------------------------------------------
# Database Configuration
# ---------------------------------------------------------------------
# Default to sqlite3 if DATABASE_URL not set
DATABASES = {
    'default': env.db(default=f'sqlite:///{BASE_DIR / "db.sqlite3"}')
}

# ---------------------------------------------------------------------
# Password validation
# ---------------------------------------------------------------------
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# ---------------------------------------------------------------------
# Internationalization
# ---------------------------------------------------------------------
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# ---------------------------------------------------------------------
# Static Files
# ---------------------------------------------------------------------
STATIC_URL = 'static/'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ---------------------------------------------------------------------
# GeoIP2 Configuration
# ---------------------------------------------------------------------
# Path where your GeoLite2-City.mmdb is located
GEOIP_PATH = os.path.join(BASE_DIR, 'geoip')

# ---------------------------------------------------------------------
# REST Framework Settings
# ---------------------------------------------------------------------
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',
    ]
}

# ---------------------------------------------------------------------
# Rate Limiting Configuration
# ---------------------------------------------------------------------
RATELIMIT_USE_CACHE = 'default'

# ---------------------------------------------------------------------
# Cache Configuration
# ---------------------------------------------------------------------
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'unique-ip-tracking-cache',
    }
}

# ---------------------------------------------------------------------
# Celery / Redis Configuration
# ---------------------------------------------------------------------
CELERY_BROKER_URL = env('CELERY_BROKER_URL', default='redis://localhost:6379/0')
CELERY_RESULT_BACKEND = CELERY_BROKER_URL
