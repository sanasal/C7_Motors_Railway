import os
from dotenv import load_dotenv
load_dotenv()

from django.core.wsgi import get_wsgi_application

settings_module = (
    'c7_motors.deployment'
    if os.environ.get('HOSTNAME')
    else 'c7_motors.settings'
)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', settings_module)

application = get_wsgi_application()