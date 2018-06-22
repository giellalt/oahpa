# -*- encoding: utf-8 -*-
"""
Django settings for LLL1_OAHPA project.

Generated by 'django-admin startproject' using Django 1.11.13.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os
import os.path
import sys

MAIN_LANGUAGE = ('sms', 'Skolt Sami')
LLL1 = MAIN_LANGUAGE[0]

os.environ['PYTHON_EGG_CACHE'] = '/tmp'
os.environ['DJANGO_SETTINGS_MODULE'] = LLL1+'_oahpa.settings'

# Confirm this is in path.
path = '/home/oahpa/'+LLL1+'_oahpa_project'
if path not in sys.path:
    sys.path.append(path)

# This flag triggers now the URL patterns in url.py file.
# The production_setting.py is triggered now by os name.
DEV = True

# Can just list the media or template dirs as here('templates') instead of '/home/me/.../smaoahpa/templates/
here = lambda x: os.path.join(os.path.abspath(os.path.dirname(sys.argv[0])), x)
here_cross = lambda x: os.path.join(os.path.abspath(os.path.dirname(sys.argv[0])), *x)

INTERNAL_IPS = ('127.0.0.1',
)

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['.gtoahpa-01.uit.no','127.0.0.1','localhost']

# Application definition

INSTALLED_APPS = [
    LLL1+'_oahpa.drill',
    LLL1+'_oahpa.courses',
    LLL1+'_oahpa.conf',
    LLL1+'_oahpa.feedback',
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
	            os.path.join(os.path.dirname(__file__), 'drill/templates').replace('\\','/'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.media',
                'django.template.context_processors.i18n',
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

LOCALE_PATHS = (
    '/home/oahpa/'+LLL1+'_oahpa_project/locale',
)

LANGUAGE_CODE = 'nb'

TIME_ZONE = 'Europe/Oslo'

USE_I18N = True

USE_L10N = True

USE_TZ = True

LANGUAGES = [
    ('sms', 'Skolt Sami'),
    ('ru', 'Russian'),
    ('sme', 'North Sami'),
	('no', 'Norwegian'),
	('en', 'English'),
	('fi', 'Finnish'),
]

OLD_NEW_ISO_CODES = {
	"fi": "fin",
	"ru": "rus",
	"en": "eng",
	"no": "nob",
	"de": "deu",
	"sv": "swe",
	"sma": "sma",
    "sme": "sme",
    "sms": "sms"
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
	#'GG': ('isme-GG.restr.fst', 'Western'),
	#'KJ': ('isme-KJ.restr.fst', 'Eastern'),
	'NG': (None, 'Non-Presented forms'),
}

DEFAULT_DIALECT = 'main'
NONGEN_DIALECT = 'NG'

if os.uname()[1] == 'gtoahpa-01.uit.no':
    LOOKUP_TOOL = '/usr/local/bin/lookup'  # xfst
    HFST_LOOKUP = '/bin/hfst-lookup' # hfst
    #LOOKUP_TOOL = '/opt/sami/xerox/c-fsm/ix86-linux2.6-gcc3.4/bin/lookup'
else:
    LOOKUP_TOOL = '/usr/local/bin/lookup'  # xfst
    HFST_LOOKUP = '/usr/local/bin/hfst-lookup'

FST_DIRECTORY = '/opt/smi/'+LLL1+'/bin'
LOG_FILE = path + '/drill/vastaF_log.txt'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

URL_PREFIX = 'nuorti'

# Absolute path to the directory that holds media.
MEDIA_ROOT = '/home/oahpa/media/'

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"

MEDIA_URL = '/%s/media/' % URL_PREFIX

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
STATIC_URL = '/home/oahpa/admin_media/'

# #
#
# USER PROFILES
#
# #

AUTH_PROFILE_MODULE = LLL1+'_oahpa.courses.UserProfile'
LOGIN_REDIRECT_URL = '/%s/courses/' % URL_PREFIX
LOGIN_URL = '/%s/courses/login/' % URL_PREFIX

CACHES = {
        'default': {
                'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
                'LOCATION': '/var/tmp/'+LLL1+'_oahpa_cache'
        },
}

# Import all var from settings that are not in svn for security reasons
from settings_not_in_svn import *
