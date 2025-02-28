import os 
from .settings import *
from .settings import BASE_DIR 
import stripe 

#The trusted urls and domains from which requests can come into our applictation 
SECRET_KEY = os.environ.get('SECRET')
ALLOWED_HOSTS = [os.environ.get('HOSTNAME')]
CSRF_TRUSTED_ORIGINS = ['https://' + os.environ.get('HOSTNAME')]

DEBUG = True


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SETTINGS_PATH = os.path.dirname(os.path.dirname(__file__))#MS ADDED
Temp_Path = os.path.realpath('.')# MS ADDED
index_path =  os.path.join(os.path.dirname(os.path.dirname(__file__)),'templates')


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(SETTINGS_PATH ,'templates')],
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

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware'
]  


STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

STATIC_URL = '/static/'
STATICFILES_DIRS=[os.path.join(BASE_DIR , 'staticfiles')]
STATIC_ROOT = os.path.join(BASE_DIR, 'static')  

DEFAULT_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage'
MEDIA_URL = "/DATA/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

# Retrieve and parse the connection string for MySQL from the environment variable
connection_string = os.environ.get("DATABASE_URL") 
if connection_string:
    parsed_url = urlparse(connection_string)

    # Extract database connection parameters from the URL
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': parsed_url.path[1:],
            'USER': parsed_url.username,
            'PASSWORD': parsed_url.password,
            'HOST': parsed_url.hostname,
            'PORT': parsed_url.port,
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': os.environ.get('MYSQL_NAME'),
            'USER': os.environ.get('MYSQL_USER'),
            'PASSWORD': os.environ.get('MYSQL_PASSWORD'),
            'HOST': os.environ.get('MYSQL_HOST'),
            'PORT': os.environ.get('MYSQL_PORT'),
        }
    }



#Payment By STRIPE
STRIPE_PUBLIC_KEY = os.environ.get('STRIPE_PUBLIC_KEY')
STRIPE_SECRET_KEY =os.environ.get('STRIPE_SECRET_KEY')