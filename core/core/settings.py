"""
Django settings for core project.

Generated by 'django-admin startproject' using Django 4.2.11.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

import os
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-&=$y0ii951b+gvto!)dn1x9z57xrvyf&yao8scpxfi^ik8p@ac'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True


ALLOWED_HOSTS = ["*"]

# Application definition
INSTALLED_APPS = [
    # 'jazzmin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework.authtoken',
    'django_filters',  # Only one instance of django_filters
    'drf_yasg',
    'user',
    'administrator',
    'sport',
    'corsheaders',
    'client_account',
    'user_main',
]


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',
]
DEBUG = True

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        # 'rest_framework.authentication.TokenAuthentication',
        'rest_framework_simplejwt.authentication.JWTAuthentication',  # Для JWT

    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',
    ],
}


ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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
DEBUG = True

WSGI_APPLICATION = 'core.wsgi.application'
CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOWED_ORIGINS = [
    "https://example.com",
    "http://localhost:3000",
    # "http://192.168.68.134:3000",  # Ваш IP-адрес для локальной сети
    # Добавьте другие домены по мере необходимости
]


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
APPEND_SLASH = False


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'ru'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, "static/")
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

DATA_UPLOAD_MAX_MEMORY_SIZE = 5242880  # 5MB


# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
# Укажите вашу кастомную модель пользователя
AUTH_USER_MODEL = 'user.CustomUser'
# ONE_C_REG = 'https://example.com/one-c-registration'  # Замените на реальный URL
# ONE_C = 'Bearer your_auth_token'  # Замените на реальный токен
#
#  # Убедитесь, что этот URL правильный
#
# # settings.py
# NIKITA_LOGIN = '12345'
# NIKITA_PASSWORD = 'e61_PO4a'
# NIKITA_SENDER = 'SMSPRO.KG'

CORS_ALLOW_METHODS = [
    'GET',
    'POST',
    'PUT',
    'DELETE',
    'PATCH',
    'OPTIONS',
]

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'kamiltaalaibekkyzy@gmail.com'
EMAIL_HOST_PASSWORD = 'nimhoxyhhkbqocmb '
# settings.py
BASE_URL = 'http://127.0.0.1:8000/admin/'

STRIPE_PUBLISHABLE_KEY = 'pk_test_51Ps1IcKVaMgv7sI2ZURWU7rW2r56h7h8afp26AVBis7KAUk7YPdosHUwBwdKqSgSg1t3Kd2U2pV4BA6s8ducs2Ey00H3WqY3Pu'
STRIPE_SECRET_KEY = 'sk_test_51Ps1IcKVaMgv7sI2c7NPQmbbJuZTdEp3akB14GZ6TuToURlTsI0aeKmX6GcPr70ACIwsYxR3psipEnt16AK1gD6s006x45h1br'