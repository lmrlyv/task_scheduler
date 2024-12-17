"""
Django settings for task_scheduler project.

Generated by 'django-admin startproject' using Django 5.1.4.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""

from pathlib import Path

from task_scheduler.utils.constants import (
    CELERY_BROKER_HOST,
    CELERY_BROKER_PASSWORD,
    CELERY_BROKER_PORT,
    CELERY_BROKER_USER,
    DB_HOST,
    DB_NAME,
    DB_PASSWORD,
    DB_PORT,
    DB_USER,
    DJANGO_SECRET_KEY,
    IS_DEBUG_ON,
)


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = DJANGO_SECRET_KEY

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = IS_DEBUG_ON

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    "django.contrib.contenttypes",
    "django.contrib.auth",
    "task_scheduler.webhook_timer",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

REST_FRAMEWORK = {
    "EXCEPTION_HANDLER": "task_scheduler.utils.exception_handler.custom_exception_handler"
}

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
        },
    },
    "loggers": {
        "task_scheduler": {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": False,
        },
        "webhook_timer": {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": False,
        },
    },
}

ROOT_URLCONF = "task_scheduler.urls"

WSGI_APPLICATION = "task_scheduler.wsgi.application"

APPEND_SLASH = True

# Celery configuration

CELERY_BROKER_URL = (
    f"amqp://{CELERY_BROKER_USER}:{CELERY_BROKER_PASSWORD}@"
    f"{CELERY_BROKER_HOST}:{CELERY_BROKER_PORT}/"
)


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "HOST": DB_HOST,
        "PORT": DB_PORT,
        "NAME": DB_NAME,
        "USER": DB_USER,
        "PASSWORD": DB_PASSWORD,
    },
    "OPTIONS": {
        "connect_timeout": 30,
    },
}


# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
