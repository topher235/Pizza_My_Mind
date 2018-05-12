#!/usr/bin/env python3
import os
import sys

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "master.settings")
    os.environ.setdefault("ADMIN_EMAIL", "raymond.sutton.15@cnu.edu")
    os.environ.setdefault("PMM_EMAIL", "mindmypizza@gmail.com")
    os.environ.setdefault("PMM_HOST", "smtp.gmail.com")
    os.environ.setdefault("PMM_PASS", "pizzaPIZZA")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)
