from os import environ
from pathlib import Path
from datetime import timedelta
from celery.schedules import crontab


BASE_DIR = Path(__file__).resolve().parent.parent

ALLOWED_HOSTS = ['*'] 

SECRET_KEY = environ.get('SECRET_KEY')
DEBUG = environ.get('DEBUG')

AUTH_USER_MODEL = 'users.CustomUser'

LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'

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

CORS_ALLOW_ALL_ORIGINS = True

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'dist', ],
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
            "hosts": [('redis://redis:6379/1')],
        },
    },
}

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework_simplejwt.authentication.JWTStatelessUserAuthentication',
    ),
    'DATETIME_FORMAT': "%d.%m.%Y %H:%M:%S",
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=300),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=3),
    'AUTH_HEADER_TYPES': ('Bearer',),
}
CSRF_TRUSTED_ORIGINS = [] 

DATABASES = {
   'default': {
       'ENGINE': environ.get('POSTGRES_ENGINE'),
       'NAME': environ.get('POSTGRES_DB'),
       'USER': environ.get('POSTGRES_USER'),
       'PASSWORD': environ.get('POSTGRES_PASSWORD'),
       'HOST': environ.get('POSTGRES_HOST'),
       'PORT': environ.get('POSTGRES_PORT'),
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

CELERY_BROKER_URL = 'redis://redis:6379/0'
CELERY_RESULT_BACKEND = "redis://redis:6379"
CELERY_IMPORTS = [
    'product_eggs.tasks.beat_app_checker',
]
CELERY_TIMEZONE = 'Europe/Moscow'
CELERY_ACCEPT_CONTENT = ['pickle', 'json']
CELERY_BEAT_SCHEDULE = {
   'applications_checker_at_11': {
       'task': 'product_eggs.tasks.beat_app_checker.applications_actual_checker',
       'schedule': crontab(hour=11, minute=00, day_of_week='mon,tue,wed,thu,fri'),
   },
} 

LANGUAGE_CODE = 'ru'
TIME_ZONE = 'Europe/Moscow'

USE_I18N = True
USE_TZ = True

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'         

STATIC_URL = "/static/" 
STATIC_ROOT = "static/"

# STATICFILES_DIRS = [
#    os.path.join(BASE_DIR, 'front/static'),
# ]

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGGING = {
        'version': 1,
        'handlers': {
            'console': {'class': 'logging.StreamHandler'}
        },
        'loggers': {
                'django.db.backends': {
                    'handlers': ['console'],
                    'level': 'DEBUG'
                    }
        } 
    }
