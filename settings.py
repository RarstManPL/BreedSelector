import os
import environ
from django.utils.translation import ugettext_lazy as _

env = environ.Env()

location = lambda x: os.path.join(
    os.path.dirname(os.path.realpath(__file__)), x)

DEBUG = env.bool('DEBUG', default=True)

ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', default=['localhost', '127.0.0.1'])

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'BreedSelectorV2',
        'USER': 'djangouser',
        'PASSWORD': 'A5F+2t#aAm3y+Kv>',
        'HOST': '127.0.0.1',
        'PORT': '3306',
    }
}

CACHES = {
    'default': env.cache(default='locmemcache://'),
}

USE_TZ = True
TIME_ZONE = 'Europe/Warsaw'

TEST_RUNNER = 'django.test.runner.DiscoverRunner'

LANGUAGE_CODE = 'pl'

LANGUAGES = (
    ('en', _('English')),
    ('pl', _('Polish')),
)

SITE_ID = 1

USE_I18N = True
USE_L10N = True

MEDIA_ROOT = location("public/media")
MEDIA_URL = '/media/'

STATIC_URL = '/static/'
STATIC_ROOT = location('public/static')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
STATICFILES_DIRS = (
    location('static/'),
)

LOCALE_PATHS = (
    location('locale/'),
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

SECRET_KEY = env.str('SECRET_KEY', default='django-insecure-c7td^f$%t2mv$o!4md2^!rov=kv-i$%bf7#okdz4re-^_si$$f')

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            location('templates'),
        ],
        'OPTIONS': {
            'loaders': [
                'admin_tools.template_loaders.Loader',
                'django.template.loaders.filesystem.Loader',
                'django.template.loaders.app_directories.Loader',
            ],
            'context_processors': [
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.request',
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.contrib.messages.context_processors.messages',
            ],
            'debug': DEBUG,
        }
    }
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',

    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',

    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.http.ConditionalGetMiddleware',
    'django.middleware.common.CommonMiddleware',
]

ROOT_URLCONF = 'urls'

INSTALLED_APPS = [
    'modeltranslation',
    'admin_tools',
    'admin_tools.theming',
    'admin_tools.menu',
    'admin_tools.dashboard',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',

    'apps.commons.apps.CommonsConfig',
    'apps.api.apps.ApiConfig',
    'apps.prediction.apps.PredictionConfig',

    'haystack',
    'adminsortable2',
    'livesettings',
    'rest_framework',
]

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
)

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {
            'min_length': 9,
        }
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
]

LOGIN_REDIRECT_URL = '/'
APPEND_SLASH = True

from django.contrib.messages import constants as messages
MESSAGE_TAGS = {
    messages.ERROR: 'danger'
}

HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.whoosh_backend.WhooshEngine',
        'PATH': location('whoosh_index'),
    },
}

INTERNAL_IPS = ['127.0.0.1', '::1']

SESSION_SERIALIZER = 'django.contrib.sessions.serializers.JSONSerializer'

SECURE_SSL_REDIRECT = env.bool('SECURE_SSL_REDIRECT', default=False)
SECURE_HSTS_SECONDS = env.int('SECURE_HSTS_SECONDS', default=0)
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True

try:
    from settings_local import *
except ImportError:
    pass

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ]
}
