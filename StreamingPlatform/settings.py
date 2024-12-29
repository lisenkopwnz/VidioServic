from pathlib import Path
import os
from datetime import timedelta
import environ
import psycopg2
import logging.config

# region ---------------------- BASE CONFIGURATION -----------------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent
env = environ.Env()
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

SECRET_KEY = env('SECRET_KEY')
DEBUG = env.bool('DEBUG', default=False)
ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', default=['localhost', '127.0.0.1'])
# endregion --------------------------------------------------------------------------------

# region ---------------------- RECOMMENDATION SERVICE-----------------------------------------
RECOMMENDATION_SERVICE_URL = env.str('RECOMMENDATION_SERVICE_URL')
API_KEY=env.str('API_KEY')
# endregion --------------------------------------------------------------------------------

# region ---------------------- CORS HEADERS -----------------------------------------------
CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_HEADERS = ['*']
CSRF_COOKIE_SECURE = False
# endregion ---------------------------------------------------------------------------------

INSTALLED_APPS = [
    # region ----------------- BASE DJANGO PACKAGES -----------
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # endregion ------------------------------------------------

    # region ----------------- REST FRAMEWORK MODULES ---------
    'rest_framework',
    'rest_framework.authtoken',
    'rest_framework_simplejwt',
    # endregion -------------------------------------------------

    # region ----------------- APPLICATIONS --------------------
    'api',  # приложения где будут все апи
    'common',  # приложения, где будут функции которые чаще используются для DRY
    # AUTH
    'accounts',
    # CONTENT
    'content',
    'comments',
    'statistic',
    'playlist',
    # PAYMENT
    'subscription',
    'payment',
    # endregion --------------------------------------------------

    'drf_spectacular',  # всегда указывать после всех других созданных приложений проекта или же в конце
    'django_elasticsearch_dsl',
    'taggit'
]

# region -------------------- MD & TEMP & WSGI & VALIDATORS & URLCONF -----------------------

MIDDLEWARE = [
    'StreamingPlatform.middleware.LoggingMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django_currentuser.middleware.ThreadLocalUserMiddleware',
    'corsheaders.middleware.CorsMiddleware',
]

ROOT_URLCONF = 'StreamingPlatform.urls'

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

WSGI_APPLICATION = 'StreamingPlatform.wsgi.application'

# endregion ------------------------------------------------------------------------

# region ---------------------- DATABASE ----------------------------------------------------
# Функция проверки доступности PostgreSQL


def is_postgres_available():
    try:
        conn = psycopg2.connect(
            dbname=env.str('DB_NAME', 'platform_base'),
            user=env.str('DB_USERNAME', 'postgres'),
            password=env.str('DB_PASSWORD', '27Fa00'),
            host=env.str('DB_HOST', 'db'),  # Используйте имя контейнера db
            port=env.int('DB_PORT', 5432),
        )
        conn.close()
        return True
    except psycopg2.OperationalError as e:
        print(f"Ошибка подключения к базе данных: {e}")
        return False


# Настройка баз данных с проверкой доступности PostgreSQL
if is_postgres_available():
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': env.str('DB_NAME', 'postgres'),
            'USER': env.str('DB_USERNAME', 'postgres'),
            'PASSWORD': env.str('DB_PASSWORD', 'postgres'),
            'HOST': env.str('DB_HOST', 'localhost'),
            'PORT': env.int('DB_PORT', 5432),
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
    }
# endregion ---------------------------------------------------------------------------------

# region ---------------------- REST FRAMEWORK ----------------------------------------------
REST_FRAMEWORK = {

    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),

    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),

    'DEFAULT_PARSER_CLASSES': (
        'rest_framework.parsers.JSONParser',
        'rest_framework.parsers.FormParser',
        'rest_framework.parsers.MultiPartParser',
        'rest_framework.parsers.FileUploadParser',
    ),

    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
}
# endregion -------------------------------------------------------------------------

# region ---------------------- SIPMLE JWT & DJOSER -----------------------------------------
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=5),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
    "ROTATE_REFRESH_TOKENS": False,
    "BLACKLIST_AFTER_ROTATION": False,
    "UPDATE_LAST_LOGIN": False,

    "ALGORITHM": "HS256",
    "SIGNING_KEY": SECRET_KEY,
    "VERIFYING_KEY": "",
    "AUDIENCE": None,
    "ISSUER": None,
    "JSON_ENCODER": None,
    "JWK_URL": None,
    "LEEWAY": 0,

    "AUTH_HEADER_TYPES": ("Bearer",),
    "AUTH_HEADER_NAME": "HTTP_AUTHORIZATION",
    "USER_ID_FIELD": "id",
    "USER_ID_CLAIM": "user_id",
    "USER_AUTHENTICATION_RULE": "rest_framework_simplejwt.authentication.default_user_authentication_rule",

    "AUTH_TOKEN_CLASSES": ("rest_framework_simplejwt.tokens.AccessToken",),
    "TOKEN_TYPE_CLAIM": "token_type",
    "TOKEN_USER_CLASS": "rest_framework_simplejwt.models.TokenUser",

    "JTI_CLAIM": "jti",

    "SLIDING_TOKEN_REFRESH_EXP_CLAIM": "refresh_exp",
    "SLIDING_TOKEN_LIFETIME": timedelta(minutes=5),
    "SLIDING_TOKEN_REFRESH_LIFETIME": timedelta(days=1),

    "TOKEN_OBTAIN_SERIALIZER": "rest_framework_simplejwt.serializers.TokenObtainPairSerializer",
    "TOKEN_REFRESH_SERIALIZER": "rest_framework_simplejwt.serializers.TokenRefreshSerializer",
    "TOKEN_VERIFY_SERIALIZER": "rest_framework_simplejwt.serializers.TokenVerifySerializer",
    "TOKEN_BLACKLIST_SERIALIZER": "rest_framework_simplejwt.serializers.TokenBlacklistSerializer",
    "SLIDING_TOKEN_OBTAIN_SERIALIZER": "rest_framework_simplejwt.serializers.TokenObtainSlidingSerializer",
    "SLIDING_TOKEN_REFRESH_SERIALIZER": "rest_framework_simplejwt.serializers.TokenRefreshSlidingSerializer",
}

DJOSER = {
    'PASSWORD_RESET_CONFIRM_URL': '#/password/reset/confirm/{uid}/{token}',
    'USERNAME_RESET_CONFIRM_URL': '#/username/reset/confirm/{uid}/{token}',
    'ACTIVATION_URL': '#/activate/{uid}/{token}',
    'SEND_ACTIVATION_EMAIL': False,
    'SERIALIZERS': {},
}
# endregion -------------------------------------------------------------------------

# region ---------------------- SPECTACULAR SETTINGS --------------------------------------
SPECTACULAR_SETTINGS = {
    'TITLE': 'STREAMING PLATFORM',
    'DESCRIPTION': 'Проект, который должен заменить YouTube и стать лучше него в СНГ',
    'VERSION': '1.0.0',
    'SERVE_PERMISSIONS': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'SERVE_AUTHENTICATION': [
        # 'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ],
    'SWAGGER_UI_SETTINGS': {
        'DeepLinking': True,
        'DisplayOperationId': True,
    },
    'COMPONENT_SPLIT_REQUEST': True,
    'SORT_OPERATIONS': False,
}
# endregion -------------------------------------------------------------------

# region ---------------------- LOCALIZATION ------------------------------------------------
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True
# endregion ----------------------------------------------------------------------------------

# region ---------------------- MEDIA AND STATIC ----------------------------------------------
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, '../', 'mediafiles')
STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, '../', 'staticfiles')
# endregion ------------------------------------------------------------------------------------

AUTH_USER_MODEL = 'accounts.User'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
AUTHENTICATION_BACKENDS = ('accounts.backends.AuthBackend',)

# region ---------------------- LOGGING CONFIG SETTINGS ----------------------------------------------
LOGGING_CONFIG = None
logging.config.dictConfig({
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'duration_file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': 'duration_request_view.log',
            'formatter': 'verbose',
        },
        'recommendation_file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': 'recommendation_system_errors.log',
            'formatter': 'verbose',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'duration_request_view': {
            'handlers': ['duration_file'],
            'level': 'INFO',
            'propagate': False,
        },
        'recommendation_system_errors':{
            'handlers': ['recommendation_file'],
            'level': 'ERROR',
            'propagate': False,
        },
        'django': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False,
        },
    },
})
# endregion ------------------------------------------------------------------------------------

# region ---------------------- ELASTICSEARCH SETTINGS ----------------------------------------------
ELASTICSEARCH_DSL = {
    'default': {
        'hosts': ['http://elasticsearch:9200'],  # Правильный ключ для указания хоста
    }
}
# endregion ------------------------------------------------------------------------------------
