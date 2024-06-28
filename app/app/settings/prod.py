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
       'NAME': os.environ.get('POSTGRES_DB'),
       'USER': os.environ.get('POSTGRES_USER'),
       'PASSWORD': os.environ.get('POSTGRES_PASSWORD'),
       'HOST': os.environ.get("DATABASE_HOST"),
       'PORT': 5432,
   }
}