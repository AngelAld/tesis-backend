"""
ASGI config for Backend project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/asgi/
"""

# tu_proyecto/asgi.py

import os
import django
from .routing import application as routing_application


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Backend.settings")

django.setup()

application = routing_application
