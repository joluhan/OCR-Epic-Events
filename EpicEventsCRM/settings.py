import os
from pathlib import Path
import sentry_sdk
from dotenv import load_dotenv

load_dotenv()

dsn = os.getenv('SENTRY_DSN')
sentry_sdk.init(
    dsn=dsn,
    enable_tracing=True,
)

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('SECRET_KEY')
TOKEN_KEY = os.getenv('TOKEN_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True # Run in debug mode (not for production)

ALLOWED_HOSTS = [] # Host/domain names that this Django site can serve


# Definition of Django applications that are activated in the project.
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # The app
    'EpicEvents',
]

# Middleware is a framework of hooks into Django's request/response processing.
MIDDLEWARE = [
    # Default Django middleware for various functionalities.
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# The root URL configuration for the project; it points to project's URL configuration module.
ROOT_URLCONF = 'EpicEventsCRM.urls'

# Django template configuration.
TEMPLATES = [
    {
        # List of directories to search for templates.
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        # Whether to look for templates inside installed applications.
        'APP_DIRS': True,
        # Context processors add variables to the context of a template.
        'OPTIONS': {
            'context_processors': [
                # Default Django context processors.
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# WSGI application path for Django's deployment.
WSGI_APPLICATION = 'EpicEventsCRM.wsgi.application'


# Database configuration.
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3', # Database engine (SQLite in this case)
        'NAME': BASE_DIR / 'db.sqlite3', # Database file path
    }
}


# Custom user model definition for authentication.
AUTH_USER_MODEL = 'EpicEvents.User'

# Password validation configuration.
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    # Validators to ensure user passwords meet certain criteria.
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


# Internationalization and localization settings.
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC' # Default time zone

USE_I18N = True # Enable Django's translation system

USE_TZ = True # Enable timezone awareness


# Static files configuration (CSS, JavaScript, Images).
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = 'static/'

# Default auto field type for models (primary keys).
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
