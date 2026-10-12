import os
from pathlib import Path
from datetime import timedelta

BASE_DIR = Path(__file__).resolve().parent.parent

def env(name, default=None):
    return os.getenv(name, default)

DEBUG = env('DEBUG','0') == '1'
SECRET_KEY = env('SECRET_KEY','unsafe-dev-secret-change-me')
ALLOWED_HOSTS = [x.strip() for x in env('ALLOWED_HOSTS','localhost,127.0.0.1').split(',') if x.strip()]

INSTALLED_APPS = [
    'django.contrib.admin','django.contrib.auth','django.contrib.contenttypes','django.contrib.sessions',
    'django.contrib.messages','django.contrib.staticfiles','corsheaders','rest_framework','django_filters',
    'drf_spectacular','accounts','organizations','projects','apis','scans','findings','reports','audit'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
ROOT_URLCONF='config.urls'
TEMPLATES=[{
    'BACKEND':'django.template.backends.django.DjangoTemplates',
    'DIRS':[BASE_DIR/'templates'],
    'APP_DIRS':True,
    'OPTIONS':{'context_processors':['django.template.context_processors.request','django.contrib.auth.context_processors.auth','django.contrib.messages.context_processors.messages']},
}]
WSGI_APPLICATION='config.wsgi.application'
ASGI_APPLICATION='config.asgi.application'

USE_SQLITE = env('USE_SQLITE', '1' if not env('POSTGRES_HOST') else '0') == '1'

if not USE_SQLITE and env('POSTGRES_HOST'):
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': env('POSTGRES_DB', 'api_sentinel'),
            'USER': env('POSTGRES_USER', 'postgres'),
            'PASSWORD': env('POSTGRES_PASSWORD', 'postgres'),
            'HOST': env('POSTGRES_HOST'),
            'PORT': env('POSTGRES_PORT', '5432'),
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

LANGUAGE_CODE='en-us'
TIME_ZONE='UTC'
USE_I18N=True
USE_TZ=True
STATIC_URL='static/'
STATIC_ROOT=BASE_DIR/'staticfiles'
MEDIA_URL='media/'
MEDIA_ROOT=BASE_DIR/'media'
DEFAULT_AUTO_FIELD='django.db.models.BigAutoField'

PASSWORD_HASHERS=['django.contrib.auth.hashers.PBKDF2PasswordHasher']
AUTH_PASSWORD_VALIDATORS=[
    {'NAME':'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME':'django.contrib.auth.password_validation.MinimumLengthValidator','OPTIONS':{'min_length':10}},
    {'NAME':'django.contrib.auth.password_validation.CommonPasswordValidator'},
]

CORS_ALLOWED_ORIGINS=[x.strip() for x in env('CORS_ALLOWED_ORIGINS','http://localhost:3000').split(',') if x.strip()]

REST_FRAMEWORK={
    'DEFAULT_AUTHENTICATION_CLASSES':['accounts.authentication.JWTAuthentication','accounts.authentication.ProjectAPIKeyAuthentication'],
    'DEFAULT_PERMISSION_CLASSES':['rest_framework.permissions.IsAuthenticated'],
    'DEFAULT_FILTER_BACKENDS':['django_filters.rest_framework.DjangoFilterBackend','rest_framework.filters.SearchFilter','rest_framework.filters.OrderingFilter'],
    'DEFAULT_PAGINATION_CLASS':'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE':25,
    'DEFAULT_SCHEMA_CLASS':'drf_spectacular.openapi.AutoSchema',
}

SPECTACULAR_SETTINGS={
    'TITLE':'API Sentinel API','DESCRIPTION':'Developer-first API security SaaS backend.','VERSION':'0.1.0',
    'SERVE_INCLUDE_SCHEMA':False,
}

JWT_ACCESS_MINUTES=int(env('JWT_ACCESS_MINUTES','30'))
JWT_REFRESH_DAYS=int(env('JWT_REFRESH_DAYS','7'))

CELERY_BROKER_URL=env('REDIS_URL','redis://redis:6379/0')
CELERY_RESULT_BACKEND=CELERY_BROKER_URL
CELERY_TASK_TRACK_STARTED=True
CELERY_TASK_TIME_LIMIT=15*60
CELERY_TASK_ALWAYS_EAGER=env('CELERY_TASK_ALWAYS_EAGER', '1' if USE_SQLITE else '0') == '1'
CELERY_TASK_EAGER_PROPAGATES=True

SECURE_SSL_REDIRECT=env('SECURE_SSL_REDIRECT','0') == '1'
SECURE_HSTS_SECONDS=31536000 if not DEBUG else 0
SECURE_HSTS_INCLUDE_SUBDOMAINS=not DEBUG
SECURE_HSTS_PRELOAD=not DEBUG
SESSION_COOKIE_SECURE=not DEBUG
CSRF_COOKIE_SECURE=not DEBUG
SECURE_CONTENT_TYPE_NOSNIFF=True
X_FRAME_OPTIONS='DENY'
SECURE_REFERRER_POLICY='same-origin'

FILE_UPLOAD_MAX_MEMORY_SIZE=5*1024*1024
DATA_UPLOAD_MAX_MEMORY_SIZE=10*1024*1024

DEFAULT_FROM_EMAIL='noreply@api-sentinel.local'
EMAIL_BACKEND='django.core.mail.backends.console.EmailBackend'
