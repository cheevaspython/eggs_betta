import os

from pathlib import Path
from datetime import timedelta
from celery.schedules import crontab
from corsheaders.defaults import default_headers

PROJECT_ROOT = Path(__file__).resolve().parent.parent

ALLOWED_HOSTS = ['*']

SECRET_KEY = os.environ.get('SECRET_KEY')
DEBUG = os.environ.get('DEBUG')

AUTH_USER_MODEL = 'users.CustomUser'

LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'

redis_port = "redis://redis:6379"

if DEBUG and os.environ.get('REDIS_PORT_CONFIG'):
    redis_port = os.environ.get('REDIS_PORT_CONFIG')

MY_APPS = [
    'users',
    'product_eggs',
    'websocket',
]

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'drf_yasg',
    'corsheaders',
    'rest_framework',

    'channels',
    'channels_postgres',
    'django.contrib.postgres',
    # 'rest_framework_simplejwt.token_blacklist',
] + MY_APPS

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

CORS_ALLOW_ALL_ORIGINS=  False
CORS_ALLOW_CREDENTIALS = True
if DEBUG:
    CORS_ALLOWED_ORIGINS = [
        "http://127.0.0.1:3000",
        "http://127.0.0.1:8000",
        "http://127.0.0.1:8080",
    ]
CORS_ALLOW_HEADERS = list(default_headers) + ['Set-Cookie']

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [PROJECT_ROOT / 'dist', ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.media',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'
ASGI_APPLICATION = 'config.asgi.application'

CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            "hosts": [(redis_port + '/1')],
        },
    },
}

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        # 'users.authenticate.CookieBasedJWTAuthentication',
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework_simplejwt.authentication.JWTStatelessUserAuthentication',
    ),
    'DATETIME_FORMAT': "%d.%m.%Y %H:%M:%S",
}

SIMPLE_JWT = {
  'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),
  'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
  'ROTATE_REFRESH_TOKENS': True,
  # 'BLACKLIST_AFTER_ROTATION': True,
  'UPDATE_LAST_LOGIN': False,

  'ALGORITHM': 'HS256',
  'SIGNING_KEY': SECRET_KEY,
  'VERIFYING_KEY': None,
  'AUDIENCE': None,
  'ISSUER': None,

  'AUTH_HEADER_TYPES': ('Bearer','JWT',),
  'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',
  'USER_ID_FIELD': 'id',
  'USER_ID_CLAIM': 'user_id',
  'USER_AUTHENTICATION_RULE': 'rest_framework_simplejwt.authentication.default_user_authentication_rule',

  'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
  'TOKEN_TYPE_CLAIM': 'token_type',

  'JTI_CLAIM': 'jti',

  'SLIDING_TOKEN_REFRESH_EXP_CLAIM': 'refresh_exp',
  'SLIDING_TOKEN_LIFETIME': timedelta(minutes=60),
  'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=1),

  # 'AUTH_COOKIE_ACCESS':'access_token',
  # 'AUTH_COOKIE_REFRESH':'refresh_token',
  # 'AUTH_COOKIE_SECURE': False,
  # 'AUTH_COOKIE_HTTP_ONLY' : True,
  # 'AUTH_COOKIE_PATH': '/',
  # 'AUTH_COOKIE_SAMESITE': 'None', #Strict
}

CSRF_USE_SESSIONS = False
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False
CSRF_COOKIE_NAME = 'csrftoken'
CSRF_COOKIE_SAMESITE = None
SESSION_COOKIE_SAMESITE = None

CSRF_TRUSTED_ORIGINS = [os.environ.get('CSRF_TRUSTED')]

DATABASES = {
   'default': {
       'ENGINE': os.environ.get('POSTGRES_ENGINE'),
       'NAME': os.environ.get('POSTGRES_DB'),
       'USER': os.environ.get('POSTGRES_USER'),
       'PASSWORD': os.environ.get('POSTGRES_PASSWORD'),
       'HOST': os.environ.get('POSTGRES_HOST'),
       'PORT': os.environ.get('POSTGRES_PORT'),
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

CELERY_BROKER_URL = redis_port + '/0'
CELERY_RESULT_BACKEND = redis_port
CELERY_IMPORTS = [
    'product_eggs.tasks.beat_app_checker',
]
CELERY_TIMEZONE = 'Europe/Moscow'
CELERY_ACCEPT_CONTENT = ['pickle', 'json']
CELERY_BEAT_SCHEDULE = {
   'applications_checker_at_11': {
       'task': 'product_eggs.tasks.beat_app_checker.applications_actual_checker',
       'schedule': crontab(
            hour="12",
            minute="00",
            day_of_week="mon,tue,wed,thu,fri"
        ),
   },
}

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.redis.RedisCache",
        "LOCATION": redis_port,
        "OPTIONS": {
            "db": "1",
        },
    }
}

BALANCE_CACHE_NAME = 'balance_entitys_cache'

LANGUAGE_CODE = 'ru'
TIME_ZONE = 'Europe/Moscow'

USE_I18N = True
USE_TZ = True

MEDIA_URL = "/media/"

if media_path := os.environ.get('MEDIA_PATH'):
    MEDIA_HDD = Path(media_path)
    MEDIA_ROOT = os.path.join(MEDIA_HDD, 'media')
else:
    MEDIA_ROOT = os.path.join(PROJECT_ROOT, 'media')

STATIC_URL = "/static/"
STATIC_ROOT =  os.path.join(PROJECT_ROOT, 'static')

STATICFILES_DIRS = [
   os.path.join(PROJECT_ROOT, "assets"),
]

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "file": {
            "level": "WARNING",
            "class": "logging.FileHandler",
            "filename": "/pilligrim/logs/debug.log",
        },
    },
    "loggers": {
        "product_eggs": {
            "handlers": ["file"],
            "level": "WARNING",
            "propagate": True,
        },
    },
}
