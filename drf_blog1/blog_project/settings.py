"""
Django settings for blog_project project.
Configured as a pure JSON API backend using DRF and JWT.
"""

from pathlib import Path
import os
from datetime import timedelta

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
SECRET_KEY = 'django-insecure-xul634bz#x5051n)rj&$p@zn8_l2wcgt$wtpx!+(94v9*st-lo'
DEBUG = True
ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions', # Needed for Django Admin
    'django.contrib.messages', # Needed for Django Admin
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework_simplejwt', # JWT Authentication
    'corsheaders',              # Cross-Origin Resource Sharing
    'blog',                     # Your application
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware', # Handles CORS headers
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware', # Needed for Django Admin
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware', # NOT needed for a stateless API
    'django.contrib.auth.middleware.AuthenticationMiddleware', # Needed for Django Admin
    'django.contrib.messages.middleware.MessageMiddleware', # Needed for Django Admin
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'blog_project.urls'

# Templates are only needed for the Django Admin site
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [], # No project-level templates needed for API
        'APP_DIRS': True, # Allows finding admin templates
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

WSGI_APPLICATION = 'blog_project.wsgi.application'


# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
AUTH_PASSWORD_VALIDATORS = [
    { 'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator', },
    { 'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator', },
    { 'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator', },
    { 'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator', },
]


# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images) - Still needed for Admin
STATIC_URL = 'static/'
# STATIC_ROOT = BASE_DIR / 'staticfiles' # Uncomment for deployment


# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# --- DRF / JWT API SETTINGS ---

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        # Use JWT authentication as the primary method for the API
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        # SessionAuth can be included if you need login to the Browsable API
        # 'rest_framework.authentication.SessionAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        # Default policy: Read-only for guests, require login (token) for writes
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    )
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60), # Access tokens expire after 1 hour
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),    # Refresh tokens expire after 1 day
}


# --- CORS SETTINGS ---
# Define which origins (frontend servers) are allowed to make requests
CORS_ALLOWED_ORIGINS = [
    "http://localhost:8001",    # Your NEW frontend Django server
    "http://127.0.0.1:8001",   # Your NEW frontend Django server (alternative IP)
    # Add other origins if needed
]
# Allow cookies and Authorization headers to be sent from these origins
# We set this to True mainly for potential future use cases, JWT doesn't strictly need it this way
CORS_ALLOW_CREDENTIALS = True


# --- MEDIA FILES ---
# Where user-uploaded files will be stored
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')