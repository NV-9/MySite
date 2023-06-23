from decouple import config, Csv
import os
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = config('SECRET_KEY')
DEBUG = config('DEBUG', cast = bool)
ALLOWED_HOSTS = list(config('ALLOWED_HOSTS', cast = Csv()))


INSTALLED_APPS = [
    'jet',
    'jet.dashboard',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'main',
    'myauth',
    'tutor',
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


CSP_STYLE_SRC = ["'self'", "cdn.jsdelivr.net",'fonts.googleapis.com','ajax.googleapis.com', 'fonts.gstatic.com','cdn.jsdelivr.net', 'cdnjs.cloudflare.com']
CSP_IMG_SRC = ["'self'",]
CSP_SCRIPT_SRC = ["'self'", "cdn.jsdelivr.net", 'ajax.googleapis.com','google.com', 'cdnjs.cloudflare.com', 'cdn.jsdelivr.net', 'maps.googleapis.com']
CSP_STYLE_SRC_ELEM = ["'self'", "cdn.jsdelivr.net", 'fonts.googleapis.com', 'fonts.gstatic.com', 'cdn.jsdelivr.net', 'cdnjs.cloudflare.com', 'unpkg.com']
CSP_FONT_SRC = ["'self'", "fonts.gstatic.com", "data:", 'cdn.jsdelivr.net', 'unpkg.com']
CSP_FRAME_SRC = ["'self'", 'www.google.com', 'google.com', 'discord.com']
CSP_INCLUDE_NONCE_IN = ["script-src",]
CSP_EXCLUDE_URL_PREFIXES = ('/admin/', '/tutor/')


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
LOGIN_URL = '/auth/login/'


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
AUTH_USER_MODEL = 'myauth.User'
SOCIAL_URLS = {
    'linkedin': 'https://www.linkedin.com/in/viswamedha-nalabotu-056852189/',
    'github': 'https://github.com/NV-9',
    'instagram': 'https://instagram.com/nalabotuviswamedha',
}


JET_THEMES = [
    {
        'theme': 'default', # theme folder name
        'color': '#47bac1', # color of the theme's button in user menu
        'title': 'Default' # theme title
    },
    {
        'theme': 'green',
        'color': '#44b78b',
        'title': 'Green'
    },
    {
        'theme': 'light-green',
        'color': '#2faa60',
        'title': 'Light Green'
    },
    {
        'theme': 'light-violet',
        'color': '#a464c4',
        'title': 'Light Violet'
    },
    {
        'theme': 'light-blue',
        'color': '#5EADDE',
        'title': 'Light Blue'
    },
    {
        'theme': 'light-gray',
        'color': '#222',
        'title': 'Light Gray'
    }
]


SENDGRID_API_KEY = config('SENDGRID_API_KEY')
EMAIL_HOST = config('EMAIL_HOST')
EMAIL_HOST_USER = config('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = SENDGRID_API_KEY
EMAIL_PORT = config('EMAIL_PORT', cast = int)
EMAIL_SEND_USER = config('EMAIL_SEND_USER')
EMAIL_USE_TLS = config('EMAIL_USE_TLS', cast = bool)



SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SESSION_EXPIRE_AT_BROWSER_CLOSE = True


SECURE_HSTS_SECONDS = 2_592_000
SECURE_HSTS_PRELOAD = True
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', "https")
SECURE_REFERRER_POLICY = "strict-origin-when-cross-origin"
REFERRER_POLICY = 'strict-origin'
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'SAMEORIGIN'