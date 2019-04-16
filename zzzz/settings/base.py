"""
Django settings for django-registration-bootstrap project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

import re
import os

from django.contrib.messages import constants as message_constants

BASE_DIR = os.path.join(os.path.dirname(__file__), '../..')

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'YOUR SECRET KEY HERE'

DEBUG = False

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'raven.contrib.django.raven_compat',
    'suit',
    'captcha',
    'registration',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'api',
    'frontend',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'zzzz.urls'

WSGI_APPLICATION = 'zzzz.wsgi.application'

FIXTURE_DIRS = [os.path.join(BASE_DIR, 'zzzz', 'fixtures')]

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

MESSAGE_TAGS = {
    message_constants.DEBUG: 'debug',
    message_constants.INFO: 'info',
    message_constants.SUCCESS: 'success',
    message_constants.WARNING: 'warning',
    # overriding this, for bootstrap:
    message_constants.ERROR: 'danger'
}


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/
SITE_ID = 1

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'frontend/static/')

TEMPLATES = [
{
    'BACKEND': 'django.template.backends.django.DjangoTemplates',
    'DIRS': [os.path.join(BASE_DIR, 'templates')],
    'APP_DIRS': True,
    'OPTIONS': {
        'context_processors': [
            'django.template.context_processors.debug',
            'django.template.context_processors.request',
            'django.contrib.auth.context_processors.auth',
            'django.contrib.messages.context_processors.messages'
        ]
    },
},]

# django-registration
LOGIN_URL = '/account/login/'
ACCOUNT_ACTIVATION_DAYS = 2
AUTH_USER_MODEL = 'api.User'
LOGIN_REDIRECT_URL = '/account/'
REGISTRATION_EMAIL_HTML = False # absolutely required so we use our custom email template, since a html one doesn't exist

RECAPTCHA_PUBLIC_KEY = 'YOUR KEY HERE'
RECAPTCHA_PRIVATE_KEY = 'YOUR KEY HERE'
NOCAPTCHA = True

AWS = {
    'access_key': '',
    'secret_key': ''
}

RESERVED_SUBDOMAINS = ['mail', '_amazonses']

USER_CLASSES = {
    0: {
        'domain_limit': 1
    },
    1: {
        'domain_limit': 5
    },
    2: {
        'domain_limit': 10
    },
    3: {
        'domain_limit': 15
    },
    4: {
        'domain_limit': 20
    },
    50: {
        'domain_limit': None
    },
}

RECORD_TYPES = {
    'A': {
        'field': 'ip',
        'regex': re.compile(r'(?:\d{1,3}\.){3}\d{1,3}')
    },
    'AAAA': {
        'field': 'ipv6',
        'regex': re.compile(r'(([0-9a-fA-F]{1,4}:){7,7}[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,7}:|([0-9a-fA-F]{1,4}:){1,6}:[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,5}(:[0-9a-fA-F]{1,4}){1,2}|([0-9a-fA-F]{1,4}:){1,4}(:[0-9a-fA-F]{1,4}){1,3}|([0-9a-fA-F]{1,4}:){1,3}(:[0-9a-fA-F]{1,4}){1,4}|([0-9a-fA-F]{1,4}:){1,2}(:[0-9a-fA-F]{1,4}){1,5}|[0-9a-fA-F]{1,4}:((:[0-9a-fA-F]{1,4}){1,6})|:((:[0-9a-fA-F]{1,4}){1,7}|:)|fe80:(:[0-9a-fA-F]{0,4}){0,4}%[0-9a-zA-Z]{1,}|::(ffff(:0{1,4}){0,1}:){0,1}((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])|([0-9a-fA-F]{1,4}:){1,4}:((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9]))')
    }
}
