from .base import *
import os
import logging.config

# Override any dev settings for production
DEBUG = False

# ============================================================================
# DATABASE CONFIGURATION
# ============================================================================
# Note: Database configuration is now handled in config/base.py
# base.py automatically checks for DATABASE_URL and configures either:
# - PostgreSQL (if DATABASE_URL is set) - used in production on DigitalOcean
# - SQLite (if DATABASE_URL is not set) - used for local development
# 
# No need to override here anymore - base.py handles all environments
# ============================================================================

# ============================================================================
# SECURITY SETTINGS FOR PRODUCTION
# ============================================================================
# These settings protect your app from common web vulnerabilities
# Only enabled in production (DEBUG=False)

# Force HTTPS everywhere
# Redirects all HTTP requests to HTTPS
# Important for protecting user data and login credentials
SECURE_SSL_REDIRECT = True

# HTTP Strict Transport Security (HSTS)
# Tells browsers to always use HTTPS for 1 year (31536000 seconds)
# Prevents "man-in-the-middle" attacks
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True  # Apply to all subdomains
SECURE_HSTS_PRELOAD = True  # Include in browser HSTS preload list

# Prevent content type sniffing
# Stops browsers from guessing file types (security issue with uploads)
SECURE_CONTENT_TYPE_NOSNIFF = True

# Enable XSS (Cross-Site Scripting) filter in browsers
# Prevents JavaScript injection attacks
SECURE_BROWSER_XSS_FILTER = True

# Secure cookies - only send over HTTPS
# Prevents cookie theft over unencrypted connections
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# Prevent clickjacking attacks
# Don't allow your app to be loaded in frames/iframes
X_FRAME_OPTIONS = 'DENY'

# ============================================================================
# EMAIL CONFIGURATION FOR PRODUCTION
# ============================================================================
# Read email settings from environment variables (set in DigitalOcean dashboard)

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = config('EMAIL_HOST', default='smtp.gmail.com')
EMAIL_PORT = config('EMAIL_PORT', default=587, cast=int)
EMAIL_USE_TLS = True  # Use TLS encryption for email
EMAIL_HOST_USER = config('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL = config('DEFAULT_FROM_EMAIL', default='noreply@propdz.com')

# ============================================================================
# LOGGING CONFIGURATION
# ============================================================================
# In production, log errors to file instead of showing detailed pages

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'WARNING',
            'class': 'logging.FileHandler',
            'filename': BASE_DIR / 'logs/django.log',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'WARNING',
            'propagate': True,
        },
    },
}
