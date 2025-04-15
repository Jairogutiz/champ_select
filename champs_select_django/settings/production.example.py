"""
Example production settings - copy this to production.py and update with your values
"""
from .base import *

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'your-secret-key-here'

DEBUG = False

ALLOWED_HOSTS = ['your-domain.com', 'your-ec2-ip']

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'your_db_name',
        'USER': 'your_db_user',
        'PASSWORD': 'your_db_password',
        'HOST': 'your_db_host',
        'PORT': '5432',
    }
}

# API endpoints
API_BASE_URL = 'https://api.your-domain.com' 