# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'pp^l$gk61x4g5afb5tc6=#0lp8u2so^$4@d#_u4_ndj!0se!#m'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'fkv_oahpa',
        'USER': 'fkv_oahpa',
        'PASSWORD': 'Kainun%',
        'HOST': 'localhost',
        'PORT': '3040',
        'OPTIONS': {
         'read_default_file': '/etc/my.cnf',
         # 'charset': 'utf8',
         'init_command': 'SET storage_engine=INNODB', #  ; SET table_type=INNODB',
         }
    }
}

FILE_CHARSET = 'utf8'
DEFAULT_CHARSET = 'utf8'
DATABASE_CHARSET =  'utf8'


if os.uname()[1] == 'gtoahpa.uit.no':
    LOOKUP_TOOL = '/usr/bin/lookup'
    FST_DIRECTORY = '/opt/smi/fkv/bin'
else:
    FST_DIRECTORY = '/Users/car010/main/langs/'+LLL1+'/gtoahpa_fst'
    LOOKUP_TOOL = '/usr/local/bin/lookup'

LOG_FILE = path + LLL1+'_oahpa/drill/vastaF_log.txt'


AUTH_PROFILE_MODULE = 'courses.UserProfile'
LOGIN_REDIRECT_URL = '/%s/courses/' % URL_PREFIX
LOGIN_URL = '/%s/courses/login/' % URL_PREFIX

CACHES = {
        'default': {
                'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
                'LOCATION': '/var/tmp/'+LLL1'_oahpa_cache'
        },
}
