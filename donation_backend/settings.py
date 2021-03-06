"""
Django settings for donation_backend project.

Generated by 'django-admin startproject' using Django 1.8.14.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
import datetime
from celery.schedules import crontab

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
# TODO
SECRET_KEY = 'j$@2aydy#$lg8^bz$og0^)j%quphld#3_4gwispzlv5r2tj^sw'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'kombu.transport.django',  # For use of celery with django database
    'reversion',
    'donation',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
)

ROOT_URLCONF = 'donation_backend.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'donation_backend.wsgi.application'


EMAIL_BACKEND = 'postmark.django_backend.EmailBackend'
POSTMARK_API_KEY = open(os.path.expanduser('~/postmark_api_key')).read().strip()
# TODO Set up EAA at Postmark
POSTMARK_SENDER = 'Ben Toner (Draftable) support@draftable.com'
POSTMARK_TEST_MODE = False
POSTMARK_TRACK_OPENS = True

AUTOMATION_START_DATE = datetime.date(2016,9,5)

# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'donation_backend',
        'USER': 'dev',
        'HOST': '',
        'PORT': '',
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

STATIC_URL = '/static/'


# We'll just use the django database for celery
# TODO don't do this, it's buggy apparently
BROKER_URL = 'django://'

# TODO work out when xero has the new bank transactions and just do once a day.
CELERYBEAT_SCHEDULE = {
    'process-transactions': {
        'task': 'donation.tasks.process_bank_transactions',
        'schedule': crontab(minute=0, hour='*/4')
    },
}

CELERY_TIMEZONE = 'UTC'

# TO run celery: celery -A donation_backend worker --beat -l info