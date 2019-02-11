# -*- coding: utf-8 -*-
"""
Django settings for fkv_oahpa project.

Generated by 'django-admin startproject' using Django 1.11.16.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

import sys
os.environ['PYTHON_EGG_CACHE'] = '/tmp'
os.environ['DJANGO_SETTINGS_MODULE'] = 'fkv_oahpa.settings'

MAIN_LANGUAGE = ('fkv', 'Kven')
LLL1 = MAIN_LANGUAGE[0]


DEV = True

INTERNAL_IPS = ('127.0.0.1',)


# Application definition

INSTALLED_APPS = [
    LLL1+'_oahpa.drill',
    LLL1+'_oahpa.conf',
    LLL1+'_oahpa.courses',
    LLL1+'_oahpa.feedback',
    LLL1+'_oahpa.management',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.locale.LocaleMiddleware',
]

ROOT_URLCONF = LLL1+'_oahpa.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(os.path.dirname(__file__), 'templates').replace('\\','/'),
    	        os.path.join(os.path.dirname(__file__), 'drill/templates').replace('\\','/'),],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.i18n',
                LLL1+"_oahpa.courses.context_processors.request_user",
				LLL1+"_oahpa.conf.context_processors.dialect",
				LLL1+"_oahpa.conf.context_processors.site_root",
				LLL1+"_oahpa.conf.context_processors.grammarlinks",
            ],
        },
    },
]

WSGI_APPLICATION = LLL1+'_oahpa.wsgi.application'


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

LANGUAGE_CODE = 'no'

TIME_ZONE = 'Europe/Oslo'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_URL = '/static/'

URL_PREFIX = 'kveeni'

MEDIA_URL = '/%s/media/' % URL_PREFIX

LANGUAGES = (
    ('fkv', 'Kven'),
    ('ru', 'Russian'),
    ('sme', 'North Sami'),
	('no', 'Norwegian'),
	#('sv', 'Swedish'),
	('en', 'English'),
	('fi', 'Finnish'),
	#('de', 'German'),
)

OLD_NEW_ISO_CODES = {
	"fi": "fin",
	"ru": "rus",
	"en": "eng",
	"no": "nob",
	"de": "deu",
	"sv": "swe",
	"sma": "sma",
    "sme": "sme",
    "fkv": "fkv"
}


INFINITIVE_SUBTRACT = {
	'nob': ur'^(?P<inf>å )?(?P<lemma>.*)$',
	'swe': ur'^(?P<inf>att )?(?P<lemma>.*)$',
	'eng': ur'^(?P<inf>to )?(?P<lemma>.*)$',
	'deu': ur'^(?P<inf>zu )?(?P<lemma>.*)$',
}

INFINITIVE_ADD = {
	'nob': ur'å \g<lemma>',
	'swe': ur'att \g<lemma>',
	'eng': ur'to \g<lemma>',
	'deu': ur'zu \g<lemma>',
}

DIALECTS = {
	'main': ('generator-oahpa-gt-norm.xfst', 'Unrestricted'),
#	'GG': ('isme-GG.restr.fst', 'Western'),
#	'KJ': ('isme-KJ.restr.fst', 'Eastern'),
	'NG': (None, 'Non-Presented forms'),
}

DEFAULT_DIALECT = 'main'
NONGEN_DIALECT = 'NG'
# # #
#
# Some settings for the install.py scripts
#
# # #

from settings_not_in_svn import *
