"""
Django settings for frontend_config project. (Frontend Django App)
"""

from pathlib import Path
import os # Make sure os is imported

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
SECRET_KEY = 'django-insecure-2hku8jyusiwr=!ve*xi1c*oes1!p6b3q)fjg9dkju+m$t4#h5$'
DEBUG = True
ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    # Add back standard apps needed for context processors & potentially templates
    'django.contrib.admin',      # Optional, but keep if you want /admin/
    'django.contrib.auth',       # Needed for 'auth' context processor
    'django.contrib.contenttypes', # Often needed by other apps
    'django.contrib.sessions',   # REQUIRED for session engine
    'django.contrib.messages',   # Needed for 'messages' context processor
    'django.contrib.staticfiles',
    'pages', # Your app name
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware', # REQUIRED for sessions
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',          # REQUIRED for forms
    'django.contrib.auth.middleware.AuthenticationMiddleware', # Needed for 'auth' context processor
    'django.contrib.messages.middleware.MessageMiddleware', # Needed for 'messages' context processor
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# Set session engine to use cookies instead of database
SESSION_ENGINE = 'django.contrib.sessions.backends.signed_cookies'

ROOT_URLCONF = 'frontend_config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')], # Correctly points to your templates
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug', # Keep debug
                'django.template.context_processors.request', # Keep request
                'django.contrib.auth.context_processors.auth',    # Needed for {{ user }} in base template
                'django.contrib.messages.context_processors.messages', # Needed for messages framework
            ],
        },
    },
]

WSGI_APPLICATION = 'frontend_config.wsgi.application'


# Database
# Defined, but not actively used for sessions. Might be used by admin/auth if kept.
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation (Not used for login/register logic, but Django checks for it)
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


# Static files (CSS, JavaScript, Images)
STATIC_URL = 'static/'
# Add STATICFILES_DIRS if you have a project-level static folder, e.g.:
# STATICFILES_DIRS = [BASE_DIR / "static"]


# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# URL for login page (used by @login_required decorator in views.py)
LOGIN_URL = 'login'
# Where to redirect after successful template login (though your view handles this)
# LOGIN_REDIRECT_URL = '/'
# Where to redirect after logout (though your view handles this)
# LOGOUT_REDIRECT_URL = '/login/'