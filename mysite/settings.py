from decouple import config, Csv
import os
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = config('SECRET_KEY')
DEBUG = config('DEBUG', cast = bool)
ALLOWED_HOSTS = list(config('ALLOWED_HOSTS', cast = Csv()))


INSTALLED_APPS = [
    'main',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'csp.middleware.CSPMiddleware',
]

CSP_STYLE_SRC = ["'self'", "cdn.jsdelivr.net",'fonts.googleapis.com','ajax.googleapis.com', 'fonts.gstatic.com',]
CSP_IMG_SRC = ["'self'",]
CSP_SCRIPT_SRC = ["'self'", "cdn.jsdelivr.net", 'ajax.googleapis.com','google.com', 'cdnjs.cloudflare.com']
CSP_STYLE_SRC_ELEM = ["'self'", "cdn.jsdelivr.net", 'fonts.googleapis.com', 'fonts.gstatic.com']
CSP_FONT_SRC = ["'self'", "fonts.gstatic.com", "data:"]
CSP_FRAME_SRC = ["'self'", 'www.google.com', 'google.com']
CSP_INCLUDE_NONCE_IN = ["script-src",]

ROOT_URLCONF = 'mysite.urls'

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


WSGI_APPLICATION = 'mysite.wsgi.application'
ASGI_APPLICATION = 'mysite.asgi.application'


POSTGRES_USER = config('POSTGRES_USER')
POSTGRES_NAME = config('POSTGRES_NAME')
POSTGRES_PASS = config('POSTGRES_PASS')
POSTGRES_HOST = config('POSTGRES_HOST')
POSTGRES_PORT = config('POSTGRES_PORT')

DATABASES = {
    'default': {
		'ENGINE': 'django.db.backends.postgresql_psycopg2',
		'NAME': POSTGRES_NAME,
		'USER': POSTGRES_USER,
		'PASSWORD': POSTGRES_PASS,
		'HOST': POSTGRES_HOST,
		'PORT': POSTGRES_PORT,
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
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True


STATIC_URL = '/static/'
STATIC_ROOT = config('STATIC_ROOT', default=os.path.join(BASE_DIR, 'static'))
MEDIA_URL = '/media/'
MEDIA_ROOT = config('MEDIA_ROOT', default=os.path.join(BASE_DIR, 'media'))


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


SECURE_HSTS_SECONDS = 2_592_000
SECURE_HSTS_PRELOAD = True
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', "https")
SECURE_REFERRER_POLICY = "strict-origin-when-cross-origin"
REFERRER_POLICY = 'strict-origin'
SECURE_CONTENT_TYPE_NOSNIFF = True
