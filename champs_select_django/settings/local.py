"""
Development-specific settings
"""
from .base import *

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-t2r0t08svhg_5ewo1feo#m@8=$d6yi^&sze+&p3$b7l57gt#-q'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# API endpoints
API_BASE_URL = 'http://localhost:8000'
# Add other local-specific settings 