"""
Django settings for medical_services project.

Generated by 'django-admin startproject' using Django 5.0.1.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

import os
from pathlib import Path
import json

# Build paths inside the project like this: BASE_DIR / 'subdir'.
# BASE_DIR = Path(__file__).resolve().parent.parent
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

if os.environ.get("SET_ENVIRONMENT") == "PRODUCTION":
    JSON_FILE_PATH = os.path.join(BASE_DIR, "settingsenv_prod.json")
elif os.environ.get("SET_ENVIRONMENT") == "SANDBOX":
    JSON_FILE_PATH = os.path.join(BASE_DIR, "settingsenv_sand.json")
else:
   JSON_FILE_PATH = os.path.join(BASE_DIR, "settingsenv.json")
STAGE = os.environ.get("SET_ENVIRONMENT")

fd = open(JSON_FILE_PATH, 'r')
jsondata = fd.read()
settings_details = json.loads(jsondata)




# Build paths inside the project like this: BASE_DIR / 'subdir'.
# BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = settings_details['SECRET_KEY']

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# ALLOWED_HOSTS = ['*']
ALLOWED_HOSTS = settings_details['ALLOWED_HOSTS']

# #Custom Auth User
# AUTH_USER_MODEL = "healthcare.User"
settings_details['AUTH_USER_MODEL'] = 'healthcare.User'

# Application definition
INSTALLED_APPS = settings_details['INSTALLED_APPS']
MIDDLEWARE = settings_details['MIDDLEWARE']

ROOT_URLCONF = 'commons.urls'

TEMPLATES = settings_details['TEMPLATES']

WSGI_APPLICATION = settings_details['WSGI_APPLICATION']


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = settings_details['DATABASES']


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = settings_details['AUTH_PASSWORD_VALIDATORS']


CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_HEADERS = [
    'authorization',
    'content-type',
    'request-id'
]

# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/


LANGUAGE_CODE = settings_details['LANGUAGE_CODE']

TIME_ZONE = settings_details['TIME_ZONE']

USE_I18N = settings_details["USE_I18N"]

USE_TZ = settings_details["USE_TZ"]



# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

# STATIC_URL = 'static/'
STATIC_URL = settings_details["STATIC_URL"]
# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# REST_FRAMEWORK = {
#     'DEFAULT_AUTHENTICATION_CLASSES': (
#         'oauth2_provider.contrib.rest_framework.OAuth2Authentication',
#     )
# }

AUTHENTICATION_BACKENDS = [
    #'healthcare.backends.CustomAuthBackend',  # Custom backend
    'healthcare.common.helper.CustomAuthBackend',
    'django.contrib.auth.backends.ModelBackend',  # Default Django backend
]

OAUTH2_PROVIDER = {
    'SCOPES': {'read': 'Read scope', 'write': 'Write scope', 'groups': 'Access to your groups'}
}

SERVER_PROTOCOLS = settings_details["SERVER_PROTOCOLS"]
AUTH_TOKEN_URL = settings_details["AUTH_TOKEN_URL"]
AUTH_TOKEN_PASSWORD = settings_details["AUTH_TOKEN_PASSWORD"]
AUTH_CLIENT_ID = settings_details["AUTH_CLIENT_ID"]
AUTH_SECRET_ID = settings_details["AUTH_SECRET_ID"]
FREESEARCH_PASSWORD = settings_details["FREESEARCH_PASSWORD"]
FREESEARCH_USERNAME = settings_details["FREESEARCH_USERNAME"]
REVOKE_TOKEN = settings_details["REVOKE_TOKEN"]

# LOGS FILE
HEALTHCARE_LOG_FILENAME = settings_details["HEALTHCARE_LOG_FILENAME"]
HEALTHCARE_EXCEPTION_LOGFILE_NAME = settings_details["HEALTHCARE_EXCEPTION_LOGFILE_NAME"]
HEALTHCARE_DEV_LOGFILE_NAME = settings_details["HEALTHCARE_DEV_LOGFILE_NAME"]
HEALTHCARE_ERROR = settings_details["HEALTHCARE_ERROR"]
LOGFILE_SIZE = 5 * 1024 * 1024
LOGFILE_COUNT = 5

# "default": {
#         "ENGINE": "django.db.backends.mysql",
#         "NAME": "medical_services",
#         "USER": "root",
#         "PASSWORD": "Mehboob@2024",
#         "HOST":"localhost",
#         "PORT":"3306"

# super_user_name = sajidAli
# password = sajid@2024
# name = "medical_services"

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'simple': {
            'format': '[%(asctime)s] %(levelname)s %(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S'
        },
        'verbose': {
            'format': '[%(asctime)s] %(levelname)s ' + ' [%(name)s.%(funcName)s:%(lineno)d] %(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S'
        },
    },
    'handlers': {
        'development_log': {
            'level': 'ERROR',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': HEALTHCARE_DEV_LOGFILE_NAME,
            'formatter': 'simple'
        },
        'healthcare_log': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'maxBytes': LOGFILE_SIZE,
            'backupCount': LOGFILE_COUNT,
            'filename': HEALTHCARE_LOG_FILENAME,
            'formatter': 'simple'
        },
        'healthcare_excp_log': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'maxBytes': LOGFILE_SIZE,
            'backupCount': LOGFILE_COUNT,
            'filename': HEALTHCARE_EXCEPTION_LOGFILE_NAME,
            'formatter': 'verbose'
        }
    },
    'loggers': {
        'entity': {
            'handlers': ['development_log'],
            'level': 'ERROR'
        },
        'django.request': {
            'handlers': ['development_log'],
            'level': 'ERROR',
            'propagate': False,
        },
        'django.db.backends': {
            'handlers': ['development_log'],
            'propagate': False,
            'level': 'ERROR',
        },
        'healthcare': {
            'handlers': ['healthcare_log'],
            'level': 'DEBUG'
        },
        'healthcare_excp': {
            'handlers': ['healthcare_excp_log'],
            'level': 'DEBUG'
        }
        # 'healthcare_cron': {
        #     'handlers': ['healthcare_cron_log'],
        #     'level': 'DEBUG'
        # },
        # 'healthcare_cron_excp': {
        #     'handlers': ['healthcare_cron_excp_log'],
        #     'level': 'DEBUG'
        # }
    }
}







EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'mehboob882831@gmail.com'
EMAIL_HOST_PASSWORD = 'cncy cupr ngtn ftjb'
EMAIL_USE_SSL = False  # Add this line
EMAIL_DEBUG = True  # Add this line
# EMAIL_FROMADDR = ""
# EMAIL_SMTP_HOST = ""
# EMAIL_SMTP_PORT = ""
