import os
from .base import *


DEBUG = True

ADMINS = [
    ('Nathan-Yinka', 'oludarenathaniel@gmail.com'),
]

ALLOWED_HOSTS = ["*"]


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DATABASE_NAME'),
        'USER': os.environ.get('DATABASE_USER'),
        'PASSWORD': os.environ.get('DATABASE_PASSWORD'),
        'HOST': os.environ.get('DATABASE_HOST'),
        'PORT': '5432',
    }
}

STATIC_ROOT = os.path.join(BASE_DIR, 'static')