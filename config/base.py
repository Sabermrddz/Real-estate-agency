from pathlib import Path
import os  # For reading environment variables
from decouple import config

# Import dj-database-url for parsing DATABASE_URL from DigitalOcean
try:
    import dj_database_url
except ImportError:
    dj_database_url = None

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = config('SECRET_KEY')
DEBUG = config('DEBUG', default=False, cast=bool)

# ALLOWED_HOSTS: Supports multiple domains
# - localhost & 127.0.0.1 for local development
# - *.ondigitalocean.app for DigitalOcean preview URLs
# - propdz.com & www.propdz.com for production
ALLOWED_HOSTS = config(
    'ALLOWED_HOSTS',
    default='localhost,127.0.0.1,*.ondigitalocean.app,propdz.com,www.propdz.com'
).split(',')

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.postgres',
    
    # Local apps
    'accounts',
    'listings',
    'messaging',
    'dashboard',
    'admin_panel',
    'core',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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

WSGI_APPLICATION = 'config.wsgi.application'

# ============================================================================
# DATABASE CONFIGURATION
# Flexible configuration that works BOTH locally (SQLite) and production (PostgreSQL)
# ============================================================================

# Strategy:
# 1. If DATABASE_URL environment variable exists (DigitalOcean provides this)
#    → Use PostgreSQL with the connection string from DigitalOcean
# 2. If DATABASE_URL doesn't exist (local development)
#    → Fall back to SQLite for easy local testing without external database server

if 'DATABASE_URL' in os.environ:
    # ========================================================================
    # PRODUCTION CONFIGURATION (DigitalOcean App Platform)
    # ========================================================================
    # DigitalOcean automatically sets DATABASE_URL when you add a PostgreSQL component
    # It looks like: postgresql://user:password@host:5432/dbname
    
    DATABASES = {
        'default': dj_database_url.config(
            # Tell dj_database_url to read the DATABASE_URL environment variable
            # This parses the connection string and converts it to Django format
            default=os.environ.get('DATABASE_URL'),
            
            # conn_max_age=600: Connection pooling
            # Keeps database connection alive for 600 seconds instead of creating
            # a new connection per request. This improves performance significantly.
            conn_max_age=600,
            
            # conn_health_checks=True: Verify connection is alive before using it
            # Prevents "connection closed by server" errors, especially after
            # database restarts. Important for reliability.
            conn_health_checks=True,
        )
    }
else:
    # ========================================================================
    # DEVELOPMENT CONFIGURATION (Local Machine)
    # ========================================================================
    # When DATABASE_URL is not set (local development), use SQLite
    # Benefits:
    # - No external database server required
    # - File-based (stored in db.sqlite3 in project root)
    # - Much faster startup time
    # - Perfect for testing and local development
    
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',  # SQLite engine
            'NAME': BASE_DIR / 'db.sqlite3',  # File location in project root
        }
    }

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Custom User Model
AUTH_USER_MODEL = 'accounts.CustomUser'

# Authentication backend to support login with username or email
AUTHENTICATION_BACKENDS = [
    'accounts.backends.EmailBackend',
    'django.contrib.auth.backends.ModelBackend',
]

# Message tags for Bootstrap 5 compatibility
# Maps Django message levels to Bootstrap alert classes
from django.contrib.messages import constants as message_constants
MESSAGE_TAGS = {
    message_constants.DEBUG: 'info',
    message_constants.INFO: 'info',
    message_constants.SUCCESS: 'success',
    message_constants.WARNING: 'warning',
    message_constants.ERROR: 'danger',  # Bootstrap uses 'danger' not 'error'
}

# Templates context processors
TEMPLATES[0]['OPTIONS']['context_processors'].append('core.context_processors.unread_counts')
