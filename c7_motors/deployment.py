import os
from .settings import *
from .settings import BASE_DIR
import stripe
from urllib.parse import urlparse 

# Security & Allowed Hosts
SECRET_KEY =  os.environ.get("SECRET")
ALLOWED_HOSTS = [os.environ.get("HOSTNAME")] 
CSRF_TRUSTED_ORIGINS = [f"https://{os.environ.get('HOSTNAME')}"]


# Debug Mode
DEBUG = True 

# Paths & Templates
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SETTINGS_PATH = os.path.dirname(os.path.dirname(__file__))  # MS ADDED
Temp_Path = os.path.realpath('.')  # MS ADDED

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
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


# Static & Media Files
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
STATIC_URL = '/static/'
STATICFILES_DIRS = os.path.join(BASE_DIR, 'staticfiles')
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

DEFAULT_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage'

MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

'''
connection_string = os.environ.get("DATABASE_URL")
if connection_string:
    parsed_url = urlparse(connection_string)

    # Extract database parameters
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': parsed_url.path[1:],  # Removes the leading '/' in the DB name
            'USER': parsed_url.username,
            'PASSWORD': parsed_url.password,
            'HOST': parsed_url.hostname,
            'PORT': parsed_url.port,
        }
    }
'''

DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.mysql',
                'NAME': 'railway',
                'USER':'root',
                'PASSWORD':'TTexxYqCvXCzaEcGMLTITgjmEfyEtQeA',
                'HOST': 'maglev.proxy.rlwy.net',
                'PORT': '3306' ,
            }
}

# Stripe Payment Configuration
STRIPE_PUBLIC_KEY = os.environ.get("STRIPE_PUBLIC_KEY")
STRIPE_SECRET_KEY = os.environ.get("STRIPE_SECRET_KEY")