
from pathlib import Path
from dotenv import load_dotenv
from django.utils.translation import gettext_lazy as _
import socket
import dj_database_url
import os

load_dotenv() # environment variable

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
TEMPLATE_DIR = os.path.join(BASE_DIR, 'templates')
STATIC_DIR = os.path.join(BASE_DIR, 'static')
FILTERS_DISABLE_HELP_TEXT = True

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-405vf4n9(92i_0f$e#33ii(^o5%l-pdr07(h1x(nxm9&vtif5w"
# SECRET_KEY = os.environ.get('SECRET_KEY')
# SECRET_KEY = os.getenv('SECRET_KEY')


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

# Languages setup
LANGUAGES = [
    ('en', _('English')),
    ('bn', _('Bengali')),
    ('ms', _('Malay')),
]

LOCALE_PATHS = [
    BASE_DIR / 'locale/',
]


# Setup restframework everythings
## Modify to abstructbase user
AUTH_USER_MODEL = 'API_authentication.User'

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        # 'rest_framework.permissions.IsAuthenticated',
        'rest_framework.permissions.AllowAny',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        # 'rest_framework.authentication.TokenAuthentication',
    ),
}


# Allow http origin 
CORS_ALLOWED_ORIGINS = [
    'http://localhost:3000', # Frontend React
    'http://127.0.0.1:8000', # Backend Django
]
CORS_ALLOW_CREDENTIALS = True
CSRF_COOKIE_SECURE = True

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # 'django.contrib.sites', # via social accounts auth
    
    # rest_framework for api creations
    'rest_framework',
    'rest_framework.authtoken',
    
    # local apps
    'event',
    'authentication',
    'API',
    'API_authentication',
    
    # to allow multiple host/domain
    'corsheaders',
    
    # crispy bootstrap
    'crispy_forms',
    'crispy_bootstrap5',
    
    # for multiple languages
    'rosetta', 
    
    # Recaptcha form validation
    'django_recaptcha',
    
    # # allauth for social accoutns
    # 'allauth',
    # 'allauth.account',
    # 'allauth.socialaccount',
    
    # # allauth social accounts providers
    # 'allauth.socialaccount.providers.facebook',
    # 'allauth.socialaccount.providers.google',
    # 'allauth.socialaccount.providers.github',
    # # 'allauth.socialaccount.providers.linkedin_oauth2',
          
]

CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"

# Recaptcha public-key and privet-key
RECAPTCHA_PUBLIC_KEY = '6Ldz5nwpAAAAALeBq1Bui6BbPRJIJcIa4mDITz4D'
RECAPTCHA_PRIVATE_KEY = '6Ldz5nwpAAAAAMiCRKM49UfcM3cy8jWRiw7pHuYM'

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',     # for allow multiple host/domain
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware', # for multiple language
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # "allauth.account.middleware.AccountMiddleware", # For social account auth

]

ROOT_URLCONF = 'EventRegistration.urls'


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEMPLATE_DIR, ],
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

WSGI_APPLICATION = 'EventRegistration.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases


localhost = socket.gethostname() in ['localhost', '127.0.0.1']
if localhost:
    # Configuration for SQLite3
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }
else:
    # Configuration for PostgreSQL
    DATABASES = {
        'default': dj_database_url.parse('postgres://guestmanagementdatabase_user:tR5TCjcsseaquCuw4VYOYJRNZziYde0t@dpg-cne8ptug1b2c739pp5p0-a.singapore-postgres.render.com/guestmanagementdatabase'),
    }


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Dhaka'

USE_I18N = True # for multiple language

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/
STATIC_ROOT = 'staticfiles'
STATIC_URL = 'static/'
STATICFILES_DIRS = [STATIC_DIR, ]

# Media file
MEDIA_ROOT = 'media/'
# MEDIA_URL = BASE_DIR / 'media'

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Email Setup
EMAIL_BACKEND       = os.environ.get("EMAIL_BACKEND")
EMAIL_HOST          = os.environ.get("EMAIL_HOST_PROVIDER")
EMAIL_USE_TLS       = os.environ.get("EMAIL_USE_TLS")
EMAIL_PORT          = os.environ.get("EMAIL_PORT")
EMAIL_HOST_USER     = os.environ.get("FROM_EMAIL")
EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_PASSWORD")