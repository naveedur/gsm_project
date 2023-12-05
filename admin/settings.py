

import os
from pathlib import Path
import re
from urllib import request
from django.conf import settings
from telnetlib import LOGOUT



import socket

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-6pep6104*d=uojqyz42m5++dx()g@(j4f(s2m$yabi@sp!ayq4'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # 'crispy_forms',
    'django.contrib.sites',
    'django.contrib.humanize',
    
    # 'admin_dashboard',
    'paypal.standard.ipn', 
    'Adsense',
    'gsmApp',
    'blogApp',
    'subscriptionApp',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    'import_export',
    'django.contrib.sitemaps',
    'django_social_share',
    # "django_check_seo",
    'taggit',
    'django_select2',
    'tagulous'
]
INSTALLED_APPS += ('django_summernote', )


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    # 'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    'subscriptionApp.middleWares.DailyDownloadLimitMiddleware',
]

ROOT_URLCONF = 'admin.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['templates'],
        'APP_DIRS': True,
        'OPTIONS': {
    
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                 'gsmApp.templatetags.context_processors.user_data',
                
            ],
            
        },
    },
]

WSGI_APPLICATION = 'admin.wsgi.application'


# postgrsql database

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'gsm', 
        'USER': 'postgres', 
        'PASSWORD': '2211',
        'HOST': '127.0.0.1', 
        'PORT': '5432',
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/


STATIC_URL = '/static/'
X_FRAME_OPTIONS='SAMEORIGN'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
# STATIC_ROOT= BASE_DIR / 'static'
MEDIA_ROOT  = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'


# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


TAGGIT_CASE_INSENSITIVE = True
TAGGIT_STRIP_UNICODE_WHEN_SLUGIFYING=True

# import export
IMPORT_EXPORT_USE_TRANSACTIONS=True


# mail server settings
SITE_ID=1
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_HOST = 'smtp.gmail.com'
# EMAIL_PORT = 587
# EMAIL_USE_TLS = True
# EMAIL_HOST_USER ='navedur1039@gmail.com'
# EMAIL_HOST_PASSWORD = 'jnazkvohhspviyte'
# # qohaprjirfbefwip


# auth
# from django.contrib.auth.models import User


LOGIN_REDIRECT_URL="/"
# currentuser=request.User
import urllib.request as urllib

# import django
# django.setup()
# if request.user.has_usable_password():
#     LOGIN_REDIRECT_URL="/"
# else:
#     LOGIN_REDIRECT_URL="socialpassword/"    



SOCIALACCOUNT_PROVIDERS = { 
    'globus': {
        'SCOPE': [
            'openid',
            'profile',
            'email',
            'urn:globus:auth:scope:transfer.api.globus.org:all'
        ]
    }
}

ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_UNIQUE_EMAIL=True



# django check seo
DJANGO_CHECK_SEO_SETTINGS = {
    "content_words_number": [300, 600],
    "internal_links": 1,
    "external_links": 1,
    "meta_title_length": [30, 60],
    "meta_description_length": [50, 160],
    "keywords_in_first_words": 50,
    "max_link_depth": 3,
    "max_url_length": 70,
}
DJANGO_CHECK_SEO_EXCLUDE_CONTENT = "tag, .class, #id, tag > .child_class"
DJANGO_CHECK_SEO_FORCE_HTTP = True
DJANGO_CHECK_SEO_AUTH = {
    "user": os.getenv("admin"),
    "pass": os.getenv("admin"),
}
DJANGO_CHECK_SEO_AUTH_FOLLOW_REDIRECTS = True



# paypal 
PAYPAL_TEST = False
PAYPAL_RECEIVER_EMAIL = 'engremran89@gmail.com'

