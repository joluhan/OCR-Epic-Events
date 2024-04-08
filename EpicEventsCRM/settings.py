from pathlib import Path  # Import Path class for filesystem paths

# Define the base directory of Django project.
BASE_DIR = Path(__file__).resolve().parent.parent

# Security settings for the Django project.
SECRET_KEY = 'django-insecure-b90yg3twbpc7=gug4q0_!810_gilx_ymi2v1ro(i^pz03bc)yx'  # Secret key for cryptographic signing
DEBUG = True  # Run in debug mode (not for production)
ALLOWED_HOSTS = []  # Host/domain names that this Django site can serve

# Definition of Django applications that are activated in the project.
INSTALLED_APPS = [
    # Default Django apps for the admin interface, authentication, etc.
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
        # Backend to render templates.
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        # List of directories to search for templates.
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
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',  # Database engine (SQLite in this case)
        'NAME': BASE_DIR / 'db.sqlite3',  # Database file path
    }
}

# Custom user model definition for authentication.
AUTH_USER_MODEL = 'EpicEvents.User'

# Password validation configuration.
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
LANGUAGE_CODE = 'en-us'  # Default language code
TIME_ZONE = 'UTC'  # Default time zone
USE_I18N = True  # Enable Django's translation system
USE_TZ = True  # Enable timezone awareness

# Static files configuration (CSS, JavaScript, Images).
STATIC_URL = 'static/'  # URL to use when referring to static files

# Default auto field type for models (primary keys).
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
