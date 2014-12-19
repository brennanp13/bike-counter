import os
from .base import BASE_DIR, INSTALLED_APPS

#INSTALLED_APPS += ('django_extensions',)
#INSTALLED_APPS += ('devserver',)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}