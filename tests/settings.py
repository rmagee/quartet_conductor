# -*- coding: utf-8
from __future__ import unicode_literals, absolute_import

import django

DEBUG = True
USE_TZ = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "#73f02j*y+l2_3^8%y+fw$my9chn#z_ida%p=p%q^0gso*_y8x"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
    }
}

ROOT_URLCONF = "tests.urls"

INSTALLED_APPS = [
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sites",
    'rest_framework',
    'material',
    'quartet_capture',
    'quartet_templates',
    "quartet_conductor",
]

SITE_ID = 1

if django.VERSION >= (1, 10):
    MIDDLEWARE = ()
else:
    MIDDLEWARE_CLASSES = ()

TELNET_HOST='telnetServer'
TELNET_PORT=23

try:
    from .local_settings import *
    print('LOCAL SETTINGS FOUND')
except ImportError:
    print('No local settings detected.')
