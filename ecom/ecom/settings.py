import os
from pathlib import Path
from decouple import config

BASE_DIR = Path(__file__).resolve().parent.parent

# ========================
# SECURITY
# ========================
SECRET_KEY = config('SECRET_KEY')
DEBUG = config('DEBUG', default=False, cast=bool)
ALLOWED_HOSTS = config('ALLOWED_HOSTS').split(',')

# ========================
# APPLICATIONS
# ========================
INSTALLED_APPS = [
    # Django apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Local apps
    'app',
    'cart',

    # Third-party apps
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'social_django',
    'khalti',
    'phonenumber_field',
]

CART_SESSION_ID = 'cart'

# ========================
# MIDDLEWARE
# ========================
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'social_django.middleware.SocialAuthExceptionMiddleware',
    'allauth.account.middleware.AccountMiddleware',
]

# ========================
# AUTH
# ========================
LOGIN_URL = "user_login"
LOGIN_REDIRECT_URL = "home"
LOGOUT_REDIRECT_URL = "signin"

AUTHENTICATION_BACKENDS = [
    'social_core.backends.google.GoogleOAuth2',
    'social_core.backends.github.GithubOAuth2',
    'django.contrib.auth.backends.ModelBackend',
]

SOCIAL_AUTH_URL_NAMESPACE = 'social'

# Social Auth Keys
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = config('GOOGLE_CLIENT_ID')
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = config('GOOGLE_CLIENT_SECRET')

SOCIAL_AUTH_GITHUB_KEY = config('GITHUB_CLIENT_ID')
SOCIAL_AUTH_GITHUB_SECRET = config('GITHUB_CLIENT_SECRET')
SOCIAL_AUTH_GITHUB_SCOPE = ['user:email']

# ========================
# URL / TEMPLATES
# ========================
ROOT_URLCONF = 'ecom.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'cart.context_processor.cart_total_amount',
            ],
        },
    },
]

WSGI_APPLICATION = 'ecom.wsgi.application'

# ========================
# DATABASE (SQLite for now)
# ========================
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# ========================
# PASSWORD VALIDATION
# ========================
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# ========================
# INTERNATIONALIZATION
# ========================
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# ========================
# STATIC & MEDIA
# ========================
STATIC_URL = '/static/'

STATICFILES_DIRS = [
    BASE_DIR / 'app' / 'static',
]

STATIC_ROOT = BASE_DIR / 'staticfiles'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# ========================
# CUSTOM USER
# ========================
AUTH_USER_MODEL = "app.User"

# ========================
# EMAIL CONFIG
# ========================
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True

EMAIL_HOST_USER = config('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')