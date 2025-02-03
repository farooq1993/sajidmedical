"""
WSGI config for medical_services project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'commons.settings')

def application(environ, start_response):
    if 'SET_ENVIRONMENT' in environ:
        os.environ.setdefault('SET_ENVIRONMENT', environ['SET_ENVIRONMENT'])
    _application = get_wsgi_application()
    return _application(environ, start_response)
