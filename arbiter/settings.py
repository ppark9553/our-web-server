'''
In our settings file, we configure everything we need to take care of dependencies
'''

import os
import _pickle as pickle

from .config import CONFIG, THIS_SYSTEM

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# import all server related information from config.py file
SECRET_KEY = CONFIG['common']['SECRET_KEY']
DB_NAME = CONFIG['common']['DB_NAME']
DB_USER = CONFIG['common']['DB_USER']
DB_PW = CONFIG['common']['DB_PW']
DEBUG = True if CONFIG['common']['DEBUG'] == 'True' else False

ALLOWED_HOSTS = ['127.0.0.1', '127.0.1.1'] # accept local connections as default

if THIS_SYSTEM == 'gateway':
    # gateway server gets a domain name of: 'minedquants.com'
    ALLOWED_HOSTS = ALLOWED_HOSTS + ['minedquants.com', 'wwww.minedquants.com', CONFIG['ip-address']['gateway']]
elif THIS_SYSTEM == 'web':
    # web server gets a domain name of: 'buzzz.co.kr'
    ALLOWED_HOSTS = ALLOWED_HOSTS + ['buzzz.co.kr', 'wwww.buzzz.co.kr', CONFIG['ip-address']['web']]
else:
    ALLOWED_HOSTS = ALLOWED_HOSTS + [CONFIG['ip-address'][THIS_SYSTEM]]

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.humanize',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_celery_beat',
    'django_celery_results',
    'rest_framework',
    'rest_framework.authtoken',

    # define arbiter specific app names here
    'stockapi',
]

if THIS_SYSTEM == 'gateway':
    INSTALLED_APPS = INSTALLED_APPS + ['gateway']
if THIS_SYSTEM == 'gobble':
    INSTALLED_APPS = INSTALLED_APPS + ['gobble']

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'arbiter.urls'

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

WSGI_APPLICATION = 'arbiter.wsgi.application'

# actual production app should say 'if DEBUG == False'
# only run on PostgreSQL when in production
if DEBUG == True:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': DB_NAME,
            'USER': DB_USER,
            'PASSWORD': DB_PW,
            'HOST': CONFIG['ip-address']['db'],
            'PORT': '',
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
    }


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

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Seoul'
USE_I18N = True
USE_L10N = True
USE_TZ = False

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static-dist/')
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static/'),
]

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')

if DEBUG == False:
    REST_FRAMEWORK = {
        'DEFAULT_RENDERER_CLASSES': (
            'rest_framework.renderers.JSONRenderer',
        )
    }

worker_user = CONFIG['common']['AMQP_USER']
worker_pw = CONFIG['common']['AMQP_PW']
# ACCESS TO::: !!!web server connects to mined server & other servers (db, gateway, mined, gobble) connect to gobble server
worker_ip_address = CONFIG['ip-address']['mined'] if (THIS_SYSTEM == 'web' or THIS_SYSTEM == 'mined') else CONFIG['ip-address']['gobble']
amqp_url = 'amqp://{0}:{1}@{2}:5672//'.format(worker_user,
                                              worker_pw,
                                              worker_ip_address)
# setup Gobble & MINED server with Rabbitmq configuration
CELERY_BROKER_URL = amqp_url
CELERY_RESULT_BACKEND = amqp_url
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = TIME_ZONE

if THIS_SYSTEM == 'web' or THIS_SYSTEM == 'db':
    # setup DB + Cache Server with Redis as cache
    # direct other servers to cache server for caches
    # ACCESS TO::: !!!only web and db servers have access to caches!!!
    CACHES = {
        "default": {
            "BACKEND": "django_redis.cache.RedisCache",
            "LOCATION": "redis://{}:6379/".format(CONFIG['ip-address']['db']),
            "OPTIONS": {
                "CLIENT_CLASS": "django_redis.client.DefaultClient",
            }
        }
    }
