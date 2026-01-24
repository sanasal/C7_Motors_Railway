import os
from .settings import *
from .settings import BASE_DIR
import stripe
from urllib.parse import urlparse 

import base64

# Load from .env if needed
from dotenv import load_dotenv
load_dotenv()

'''creds_b64 = os.getenv("GOOGLE_CREDENTIALS_B64")

if creds_b64:
    path = "c7_motors/credentials/sheets.json"
    os.makedirs(os.path.dirname(path), exist_ok=True)  # Ensure folder exists
    with open(path, "wb") as f:
        f.write(base64.b64decode(creds_b64))
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = path'''

# Security & Allowed Hosts
SECRET_KEY =  os.environ.get('SECRET')
ALLOWED_HOSTS = [os.environ.get('HOSTNAME')] 
CSRF_TRUSTED_ORIGINS = ['https://' + os.environ.get('HOSTNAME')]


# Debug Mode
DEBUG = os.environ.get('DEBUG', 'False') == 'True'

# Paths & Templates
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SETTINGS_PATH = os.path.dirname(os.path.dirname(__file__))  # MS ADDED
Temp_Path = os.path.realpath('.')  # MS ADDED

INSTALLED_APPS = [
    'simple_history',
    'jazzmin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'c7_motors',
    'c7_app.apps.C7AppConfig',
    'compressor'
]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(SETTINGS_PATH, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# Middleware
MIDDLEWARE = [
    'simple_history.middleware.HistoryRequestMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.gzip.GZipMiddleware',
    'c7_app.middleware.exception_middleware.ExceptionMiddleware',
]


# Static & Media Files
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR , 'staticfiles')]
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.environ.get('MEDIA_ROOT')


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.environ.get('MYSQL_NAME'),
        'USER': os.environ.get('MYSQL_USER'),
        'PASSWORD': os.environ.get('MYSQL_PASSWORD'),
        'HOST': 'localhost',
        'PORT': '3306',
        'OPTIONS': {
            'connect_timeout': 10,
            'read_timeout': 60,
            'write_timeout': 60,
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
        },
        'CONN_MAX_AGE': 300
    }
}


# SECURITY HEADERS
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_BROWSER_XSS_FILTER = True
X_FRAME_OPTIONS = 'DENY'
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True



# Stripe Payment Configuration
STRIPE_PUBLIC_KEY = os.environ.get("STRIPE_PUBLIC_KEY")
STRIPE_SECRET_KEY = os.environ.get("STRIPE_SECRET_KEY")