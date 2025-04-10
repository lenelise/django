"""
Django settings for mysecondproject project.

Generated by 'django-admin startproject' using Django 5.1.6.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""

from pathlib import Path
from datetime import timedelta
import environ, os

env = environ.Env(
    DEBUG=(bool, False)
)

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent #the top mysecondproject directory
ENV_PATH = BASE_DIR / ".env"
environ.Env.read_env(ENV_PATH)  # Read the .env file


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-^v3ok2xt8i!ih9_ii@ioyr58lz4z0d3-w7ox%=l0z%z=$^1$7v'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    "accounts",
    "expensetracker", 
    'rest_framework', 
    'api',
    'crispy_forms',
    'crispy_bootstrap4',
    'drf_yasg',
    'rest_framework_simplejwt',
    'django_filters', 
    'django_extensions']

AUTH_USER_MODEL = "accounts.CustomUser" #we use a custom user model

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.SessionAuthentication' #required for browsable APIs
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle'
    ],
    'DEFAULT_THROTTLE_RATES': {
        'anon': '100/day',
        'user': '1000/day'
    },
    'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend']

}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(days=5),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),  
    "AUTH_HEADER_TYPES": ["Bearer"]  
}

SWAGGER_SETTINGS = {
    'DISPLAY_OPERATION_ID': False,  # Ensure operation descriptions are shown directly,
    'DEFAULT_MODEL_RENDERING': 'model',
    'USE_SESSION_AUTH': False, #Disable django login as authentication
    'SUPPORTED_SUBMIT_METHODS': [], #disables "Try it out"
}

# CRON_CLASSES = [
#     "expensetracker.cron.MyFirstCronJob",
# ]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'mysecondproject.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / "templates"],
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

WSGI_APPLICATION = 'mysecondproject.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

CRISPY_TEMPLATE_PACK = 'bootstrap4'
CRISPY_ALLOWED_TEMPLATE_PACKS = 'bootstrap4'

LOGIN_REDIRECT_URL = '/'
LOGIN_URL = '/login/'

LOGOUT_REDIRECT_URL = "home" 


#Not sure that this logging thing does anything, or if I just dont know how to use it: 
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "file": {
            "class": "logging.FileHandler",
            "filename": env('DJANGO_LOG_FILE'),
            "level": env('DJANGO_LOG_LEVEL'),
            "formatter": "simple"
        },
        "console": {
            "class": "logging.StreamHandler",
            "level": env('DJANGO_LOG_LEVEL'), #NOT WRITING EVERYTHING TO TERMINAL
            "formatter": "simple"
        }
    },
    "loggers": {
        '': { #catch all empty string, we want all log output to be sent to this logger 
            "level": env('DJANGO_LOG_LEVEL'),
            "level": "DEBUG",
            "handlers": ["file", "console"]
        }
    }, 
    "formatters": {
        "simple": {
            "format": " {asctime}: {levelname} | {module} | line {lineno}| {message}",
            "style": "{"
        }
    }
}