#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import dj_database_url
from wger.settings_global import *
from decouple import config
# Use 'DEBUG = True' to get more details for server errors
DEBUG = True
TEMPLATES[0]['OPTIONS']['debug'] = True

ADMINS = (
    ('Your name', 'your_email@example.com'),
)
MANAGERS = ADMINS

# load static files
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

STATIC_ROOT = os.path.join(PROJECT_ROOT, 'static')
STATIC_URL = '/wger/static/'

DATABASES = {
    'default': dj_database_url.config(default=config('DATABASE_URL'))
}

# Make this unique, and don't share it with anybody.
SECRET_KEY = config('SECRET_KEY')

# Your reCaptcha keys
RECAPTCHA_PUBLIC_KEY = ''
RECAPTCHA_PRIVATE_KEY = ''
NOCAPTCHA = True

# The site's URL (e.g. http://www.my-local-gym.com or http://localhost:8000)
# This is needed for uploaded files and images (exercise images, etc.) to be
# properly served.
SITE_URL = 'http://localhost:8000'

# Path to uploaded files
# Absolute filesystem path to the directory that will hold user-uploaded files.
MEDIA_ROOT = '/Users/chrismaina/.local/share/wger/media'
MEDIA_URL = '/media/'

# Allow all hosts to access the application. Change if used in production.
ALLOWED_HOSTS = '*'

# This might be a good idea if you setup memcached
# SESSION_ENGINE = "django.contrib.sessions.backends.cache"

# Configure a real backend in production
if DEBUG:
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Sender address used for sent emails
WGER_SETTINGS['EMAIL_FROM'] = 'wger Workout Manager <wger@example.com>'

# Your twitter handle, if you have one for this instance.
# WGER_SETTINGS['TWITTER'] = ''
