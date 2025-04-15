"""
Production settings for EC2 deployment
"""
from .base import *
import os

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '!*+rv65elu#i&y$!8y)t)4(mc@*3=!pv_)xsy81kfp+6(oc5!u'

DEBUG = False

ALLOWED_HOSTS = [
    'ec2-3-129-217-58.us-east-2.compute.amazonaws.com',
    '3.129.217.58',
    'localhost',
    '127.0.0.1'
]

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATIC_ROOT = str(BASE_DIR / 'staticfiles')
STATICFILES_DIRS = [
    BASE_DIR / 'static',
]

# API endpoints
API_BASE_URL = 'http://ec2-3-129-217-58.us-east-2.compute.amazonaws.com'

# Additional production settings
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
SECURE_SSL_REDIRECT = False  # Set to True if you set up HTTPS
