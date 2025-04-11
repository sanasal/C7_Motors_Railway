import os
from .settings import *
from .settings import BASE_DIR
import stripe
from urllib.parse import urlparse 


# Security & Allowed Hosts
SECRET_KEY =  os.environ.get("SECRET")
ALLOWED_HOSTS = [os.environ.get('HOSTNAME')] 
CSRF_TRUSTED_ORIGINS = ['https://' + os.environ.get('HOSTNAME')]


# Debug Mode
DEBUG = os.environ.get("DEBUG") 

# Get the PORT from environment variables (Railway uses 8080)
PORT = os.environ.get("PORT", 8080)

# Run Django with this port
if __name__ == "__main__":
    from django.core.management import execute_from_command_line
    execute_from_command_line(["manage.py", "runserver", f"0.0.0.0:{PORT}"])

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
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


# Static & Media Files
STATICFILES_STORAGE = 'whitenoise.storage.StaticFilesStorage'
STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR , 'staticfiles')]
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join("/app/media")

connection_string = os.environ.get("DATABASE_URL")
if connection_string:
    parsed_url = urlparse(connection_string)

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': parsed_url.path[1:],
            'USER': parsed_url.username,
            'PASSWORD': parsed_url.password,
            'HOST': parsed_url.hostname,
            'PORT': parsed_url.port,
            'OPTIONS': {
                'connect_timeout': 10,
                'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
            },
            'CONN_MAX_AGE': 300
        }
    }

else:

    DATABASES = {
        'default': {
                'ENGINE': 'django.db.backends.mysql',
                'NAME': os.environ.get('MYSQL_DATABASE'),
                'USER': os.environ.get('MYSQL_USER'),
                'PASSWORD': os.environ.get('MYSQL_PASSWORD'),
                'HOST': os.environ.get('MYSQL_HOST'),
                'PORT': os.environ.get('MYSQL_PORT'),
                'OPTIONS': {
                'connect_timeout': 10,
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