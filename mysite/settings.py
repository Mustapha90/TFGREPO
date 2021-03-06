# -*- coding: utf-8 -*-

"""
Django settings for mysite project.

Generated by 'django-admin startproject' using Django 1.11.1.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os
from decouple import config
import dj_database_url


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))



# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/



# Variable de entorno que ayuda a determinar si el entorno es Heroku
ON_HEROKU = 'ON_HEROKU' in os.environ


if ON_HEROKU:  

    # Obtener la clave secreta desde la variable de entorno SECRET_KEY
    SECRET_KEY = config('SECRET_KEY')

    # Deshabilitar la depuración
    DEBUG = config('DEBUG', default=True, cast=bool)

    # Configuración de la base de datos Postgres usando la variable de entorno DATABASE_URL
    DATABASES = {
          'default': dj_database_url.config(
           default=config('DATABASE_URL')
          )
    }

    # Permitir el acceso externo
    ALLOWED_HOSTS = ['*']

#Configuración para el entorno de desarrollo
else:
	# SECURITY WARNING: keep the secret key used in production secret!
	SECRET_KEY = '+_gff1)wk_b!0042x6x3=u5mr^8^y!kw*vz^yh+70cyg7l(hs&'

	# No permitir el acceso externo
	ALLOWED_HOSTS = []

    # Habilitar la depuración
	DEBUG = True

    # Usar la base de datos sqlite3
	# Database
	# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

	DATABASES = {
	    'default': {
	        'ENGINE': 'django.db.backends.sqlite3',
	        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
	    }
	}

	EMAIL_HOST = 'smtp.gmail.com'
	EMAIL_PORT = 587
	EMAIL_HOST_USER = 'xxxx@gmail.com'
	EMAIL_HOST_PASSWORD = 'xxxxx'
	EMAIL_USE_TLS = True
	EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'




# Application definition

INSTALLED_APPS = [
    'festivalapp.apps.FestivalappConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'widget_tweaks',
	'formtools',
	'django_countries',
	'bootstrap_datepicker',
    'paypal.standard.ipn',
    'table',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'mysite.urls'

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
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'mysite.wsgi.application'





# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'es'

TIME_ZONE = 'Europe/Madrid'

USE_I18N = True
USE_L10N=True


USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_ROOT = os.path.join(PROJECT_DIR, 'static')
STATIC_URL = '/static/'
STATICFILES_DIRS = ( os.path.join('static'), )
STATICFILES_STORAGE = 'whitenoise.django.GzipManifestStaticFilesStorage'





AUTH_USER_MODEL = 'festivalapp.User'

AUTH_PROFILE_MODULE = 'festivalapp.Profile'

PAYPAL_TEST = True
PAYPAL_RECEIVER_EMAIL = 'mj4ever001@gmail.com'

MEDIA_URL = '/static/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'static/media')





