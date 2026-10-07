"""WSGI config for the Tecnsol project."""
import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tecnsol.settings')
application = get_wsgi_application()
