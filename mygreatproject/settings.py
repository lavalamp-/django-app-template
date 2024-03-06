"""
Django settings for mygreatproject project.
"""
import os
from pathlib import Path
from sys import platform

import dj_database_url
import dotenv

dotenv.load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-%l#qoa47ij=glg2oytpy7qmd@usoqfij2-ssyhivdj2*wsqfkh"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get(
    "DEBUG",
    # Default to debug only in MacOS (running on developer machine).
    platform == "darwin",
)


ALLOWED_HOSTS = [
    "mygreatproject.herokuapp.com",
]
if DEBUG:
    ALLOWED_HOSTS += ["127.0.0.1", f"{os.getenv('USER')}.local"]


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "mygreatproject",
    "drf_yasg",
    "rest_framework.authtoken",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "mygreatproject.urls"

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

WSGI_APPLICATION = "mygreatproject.wsgi.application"


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

PSQL_USER = os.getenv("PSQL_USER", "postgres:postgres")
DATABASE_URL = os.environ.get(
    "DATABASE_URL", f"postgres://{PSQL_USER}@localhost/mygreatproject"
)
DATABASE_URL_POOL = os.environ.get("DATABASE_CONNECTION_POOL_URL", default=None)

PARSED_DB_DICT = dj_database_url.parse(
    DATABASE_URL_POOL or DATABASE_URL, conn_max_age=600
)
# psycopg2 issue - https://stackoverflow.com/questions/62216837
PARSED_DB_DICT["DISABLE_SERVER_SIDE_CURSORS"] = True

DATABASES = {
    "default": PARSED_DB_DICT,
}

# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = "static/"

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# Swagger / OpenAPI

SWAGGER_SCHEMA_TITLE = os.getenv("SWAGGER_SCHEMA_TITLE", "MyGreatProject API")
SWAGGER_SCHEMA_VERSION = os.getenv("SWAGGER_SCHEMA_VERSION", "v0.1")
SWAGGER_SCHEMA_DESCRIPTION = os.getenv("SWAGGER_SCHEMA_DESCRIPTION", "MyGreatProject")
SWAGGER_SETTINGS = {
    "DEFAULT_AUTO_SCHEMA_CLASS": "mygreatproject.util.openapi.MyGreatProjectAutoSchema",
    "DEFAULT_GENERATOR_CLASS": "mygreatproject.util.openapi.MyGreatProjectOpenAPISchemaGenerator",
    "DEFAULT_INFO": "mygreatproject.util.openapi.schema_info",
    "DEFAULT_API_URL": "http://127.0.0.1:8000/",
}


# User Setup

AUTH_USER_MODEL = "mygreatproject.User"

# DRF

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.TokenAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
}
