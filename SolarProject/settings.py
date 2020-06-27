"""
Django settings for SolarProject project.

Generated by 'django-admin startproject' using Django 3.0.4.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "uojp%c%-@l$aj0qc(v7(h3v63001h8$n=3g$7^g0j!)w-$#)r0"

# SECURITY WARNING: don't run with debug turned on in production!

ALLOWED_HOSTS = ["solarprojectaa.herokuapp.com", "127.0.0.1"]

# Application definition

INSTALLED_APPS = [
    "widget_tweaks",
    "design.apps.DesignConfig",
    "user.apps.UserConfig",
    "home.apps.HomeConfig",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # "django.contrib.formtools",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django_session_timeout.middleware.SessionTimeoutMiddleware",
]

ROOT_URLCONF = "SolarProject.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "SolarProject.wsgi.application"

# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",  # on utilise l'adaptateur postgresql
        "NAME": "pv",  # le nom de notre base de donnees creee precedemment
        "USER": "postgres",  # attention : remplacez par votre nom d'utilisateur
        "PASSWORD": "arnaud06",
        "HOST": "",
        "PORT": "5432",
    }
}

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.core.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.request",
)

# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

AUTH_USER_MODEL = "user.User"

LOGIN_URL = "user:login"

LOGIN_REDIRECT_URL = "home:index"

SESSION_EXPIRE_SECONDS = 3600  # 1 hour

SESSION_EXPIRE_AFTER_LAST_ACTIVITY = True

SESSION_TIMEOUT_REDIRECT = "home:index"

# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

CRISPY_TEMPLATE_PACK = "bootstrap4"

LANGUAGE_CODE = "fr-FR"

TIME_ZONE = "Europe/Paris"

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = "/static/"

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
    "/design/static/",
]

INTERNAL_IPS = ["127.0.0.1"]
DEBUG = True
SESSION_EXPIRE_AT_BROWSER_CLOSE = True

if os.environ.get("ENV") == "PRODUCTION":  # pragma: no cover
    import dj_database_url

    SECRET_KEY = os.environ.get("SECRET_KEY")
    # Static files settings
    PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

    STATIC_ROOT = os.path.join(PROJECT_ROOT, "staticfiles")

    # Extra places for collectstatic to find static files.
    STATICFILES_DIRS = (os.path.join(PROJECT_ROOT, "static"),)

    STATICFILES_STORAGE = (
        "whitenoise.storage.CompressedManifestStaticFilesStorage"
    )

    db_from_env = dj_database_url.config(conn_max_age=500)
    DATABASES["default"].update(db_from_env)
    METEOSTAT_API_KEY = os.environ["METEOSTAT_API_KEY"]
    NREL_API_KEY = os.environ["NREL_API_KEY"]
    GOOGLE_API_KEY = os.environ["GOOGLE_API_KEY"]
    OPEN_CAGE_DATA_API_KEY = os.environ["OPEN_CAGE_DATA_API_KEY"]

    sentry_sdk.init(
        dsn="https://de2f68750ba8434780281da7e05115bd@o379406.ingest.sentry.io/5285795",
        integrations=[DjangoIntegration()],
    )
else:
    from SolarProject.local_settings import (
        METEOSTAT_API_KEY,
        NREL_API_KEY,
        GOOGLE_API_KEY,
        OPEN_CAGE_DATA_API_KEY,
    )
