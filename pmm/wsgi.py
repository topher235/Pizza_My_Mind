"""
WSGI config for pmm project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "pmm.settings")
os.environ.setdefault("ADMIN_EMAIL", "raymond.sutton.15@cnu.edu")
os.environ.setdefault("PMM_EMAIL", "mindmypizza@gmail.com")
os.environ.setdefault("PMM_HOST", "smtp.gmail.com")
os.environ.setdefault("PMM_PASS", "pizzaPIZZA")

application = get_wsgi_application()
