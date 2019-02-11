# -*- encoding: utf-8 -*-
"""
Django settings for lll1_oahpa project.

Generated by 'django-admin startproject' using Django 1.11.16.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os
import os.path
import sys

MAIN_LANGUAGE = ('vro', 'Võro')
LLL1 = MAIN_LANGUAGE[0]

os.environ['PYTHON_EGG_CACHE'] = '/tmp'
os.environ['DJANGO_SETTINGS_MODULE'] = LLL1+'_oahpa.settings'

DEV = True

INTERNAL_IPS = ('127.0.0.1',)


# Application definition

INSTALLED_APPS = [
    LLL1+'_oahpa.drill',
    LLL1+'_oahpa.conf',
    LLL1+'_oahpa.courses',
    #'vro_oahpa.vro_feedback',
    LLL1+'_oahpa.management',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
	'django.contrib.sites',
    #'gunicorn',
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
    'django.contrib.admindocs.middleware.XViewMiddleware',
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
                'django.template.context_processors.media',
                'django.template.context_processors.i18n',
                'django.template.context_processors.static',
                LLL1+'_oahpa.courses.context_processors.request_user',
                LLL1+'_oahpa.conf.context_processors.dialect',
                LLL1+'_oahpa.conf.context_processors.site_root',
                LLL1+'_oahpa.conf.context_processors.grammarlinks',
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

LANGUAGE_CODE = 'nb'

TIME_ZONE = 'Europe/Oslo'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_URL = '/static/'

URL_PREFIX = 'voro'
# URL_PREFIX = '책arjel'

# Absolute path to the directory that holds media.
#MEDIA_ROOT = "/home/vro_oahpa/vro_oahpa/media/"
#MEDIA_ROOT = here('media')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"

MEDIA_URL = '/%s/media/' % URL_PREFIX



LANGUAGES = (
    ('ru', 'Russian'),
    ('sme', 'North Sami'),
    ('vro', 'Võro'),
	('no', 'Norwegian'),
	('en', 'English'),
	('fi', 'Finnish'),
    ('et', 'Estonian'),
    ('lv', 'Latvian'),
)

OLD_NEW_ISO_CODES = {
	"fi": "fin",
	"ru": "rus",
	"en": "eng",
	"et": "est",
	"no": "nob",
    "nb": "nob",
    "da": "dan",
	"de": "deu",
	"sv": "swe",
	"sma": "sma",
    "sme": "sme",
    "sjd": "sjd",
    "vro": "vro",
    "lv": "lat",
}

# Regular expression and language code. Regexp must apply 'inf' group to
# matched string.

# If infinitive is None, then we assume there is no similar infinitive
# presentation marking, or that it comes from tags for languages which
# have word forms in the system.


INFINITIVE_SUBTRACT = {
	'nob': ur'^(?P<inf>책 )?(?P<lemma>.*)$',
	'swe': ur'^(?P<inf>att )?(?P<lemma>.*)$',
	'eng': ur'^(?P<inf>to )?(?P<lemma>.*)$',
	'deu': ur'^(?P<inf>zu )?(?P<lemma>.*)$',
	'dan': ur'^(?P<inf>at )?(?P<lemma>.*)$',
}

INFINITIVE_ADD = {
	'nob': ur'책 \g<lemma>',
	'swe': ur'att \g<lemma>',
	'eng': ur'to \g<lemma>',
	'deu': ur'zu \g<lemma>',
	'dan': ur'at \g<lemma>',
}

DIALECTS = {
	'main': ('', 'Unrestricted'),
	#'GG': ('isme-GG.restr.fst', 'Western'),
	#'KJ': ('isme-KJ.restr.fst', 'Eastern'),
	'NG': (None, 'Non-Presented forms'),
}

DEFAULT_DIALECT = 'GG'
NONGEN_DIALECT = 'NG'

from settings_not_in_svn import *
