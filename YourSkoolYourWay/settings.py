
from decouple import config

from pathlib import Path
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)

BASE_DIR = Path(__file__).resolve(strict=True).parent.parent


SECRET_KEY = config("SECRET_KEY")
DEBUG = True

ALLOWED_HOSTS = config("ALLOWED_HOSTS",cast=lambda values : [value.strip() for value in values.split(",")])


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!

# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "django_extensions",
    "django_filters",
    "drf_yasg",
    "dbbackup",
    "corsheaders",
    "user",
    "school",
    "courses",
    "payment",
]

DBBACKUP_STORAGE = 'django.core.files.storage.FileSystemStorage'
DBBACKUP_STORAGE_OPTIONS = {'location': BASE_DIR/'backup'}

GRAPH_MODELS = {
    "all_applications": True,
    "group_models": True,
}




MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    'corsheaders.middleware.CorsMiddleware',
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]
ROOT_URLCONF = "YourSkoolYourWay.urls"
CORS_ORIGIN_ALLOW_ALL = True # If this is used then `CORS_ORIGIN_WHITELIST` will not have any effect
CORS_ALLOW_METHODS = config("CORS_ALLOW_METHODS",cast=lambda values : [value.strip() for value in values.split(",")])

CORS_ALLOW_HEADERS = config("CORS_ALLOW_HEADERS",cast=lambda values : [value.strip() for value in values.split(",")])
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": ["templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

JWT_AUTH = {
    "JWT_AUTHENTICATION_PREFIX": config("JWT_AUTHENTICATION_PREFIX"),
    "JWT_AUTHORIZATION_PREFIX": config("JWT_AUTHORIZATION_PREFIX"),
    "JWT_TOKEN_EXPIRATION_TIME_IN_SECONDS": config(
        "JWT_TOKEN_EXPIRATION_TIME_IN_SECONDS", cast=int
    ),
    "JWT_TOKEN_EXPIRATION_TIME_IN_MINUTES": config(
        "JWT_TOKEN_EXPIRATION_TIME_IN_MINUTES", cast=int
    ),
    "JWT_TOKEN_EXPIRATION_TIME_IN_HOURS": config(
        "JWT_TOKEN_EXPIRATION_TIME_IN_HOURS", cast=int
    ),
    "JWT_TOKEN_EXPIRATION_TIME_IN_DAYS": config(
        "JWT_TOKEN_EXPIRATION_TIME_IN_DAYS", cast=int
    ),
}


WSGI_APPLICATION = "YourSkoolYourWay.wsgi.application"


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases


# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "static"


CELERY_BROKER_URL = (
    f'redis://:{config("REDIS_PASSWORD")}@{config("REDIS_URL")}:{config("REDIS_PORT")}'
)
CELERY_RESULT_BACKEND = (
    f'redis://:{config("REDIS_PASSWORD")}@{config("REDIS_URL")}:{config("REDIS_PORT")}'
)
CELERY_ACCEPT_CONTENT = ["application/json"]
CELERY_RESULT_SERIALIZER = "json"
CELERY_TASK_SERIALIZER = "json"

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"


PAGINATION = {
    "page": config("PAGE", cast=int),
    "page_size": config("PAGE_SIZE", cast=int),
}


# twiilio sms sending API
SMS = {
    "account_sid": config(""),
    "auth_token": config("auth_token"),
    "from_number": config("from_number"),
}


SWAGGER_SETTINGS = {
    "SECURITY_DEFINITIONS": {
        "User Authentication": {
            "in": "header",
            "type": "apiKey",
            "name": "Authentication",
        },
        "Bearer JWT Token": {"in": "header", "type": "apiKey", "name": "Authorization"},
    },
    "DOC_EXPANSION": "none",
    "USE_SESSION_AUTH": False,
}


REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": ["user.authentications.JWTAuthentication"],
    "NON_FIELD_ERRORS_KEY": "error",
    "DEFAULT_PAGINATION_CLASS": "YourSkoolYourWay.customization.paginate.CustomLimitOffsetPagination",
    "PAGE_SIZE": 100,
    "EXCEPTION_HANDLER": "YourSkoolYourWay.customization.exception.my_custom_exception",
    "ORDERING_PARAM": "sort",
    'DEFAULT_FILTER_BACKENDS': ['YourSkoolYourWay.customization.filters.CustomFilter','rest_framework.filters.SearchFilter','rest_framework.filters.OrderingFilter','YourSkoolYourWay.customization.filters.CustomFilter2']

}

DEFAULT_AUTO_FIELD= 'django.db.models.AutoField'

EMAIL_BACKEND ='django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_HOST_USER = 'yourskoolyourway@gmail.com'
EMAIL_HOST_PASSWORD = 'yourskool#321'


'''REACT URL SETUP
==============='''

REACT_FRONTEND_PASSWORD_SET_URL = config("REACT_FRONTEND_PASSWORD_SET_URL")



OTP_EXPIRATION_TIME_IN_MINUTES = config("OTP_EXPIRATION_TIME_IN_MINUTES",cast=float) # e.g 3 minutes or 1.5 minutes
OTP_DIGITS_LENGTH = config("OTP_DIGITS_LENGTH",cast=int)       # e.g 123897 (max_digit=10)


### DATABASE SETTINGS

# DATABASES = {
#     "default": {
#         "ENGINE": "django.db.backends.mysql",
#         "NAME": config("DB_NAME"),
#         "USER": config("DB_USER"),
#         "PASSWORD": config("DB_PASSWORD"),
#         "HOST": config("DB_HOST"),
#         "PORT": config("DB_PORT"),
#     }
# }

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR/"db.sqlite3",
    }
}



DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

AWS_ACCESS_KEY_ID = config('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = config('AWS_SECRET_ACCESS_KEY')
AWS_S3_REGION_NAME = config('AWS_S3_REGION_NAME')
AWS_STORAGE_BUCKET_NAME = config('AWS_STORAGE_BUCKET_NAME')
EMAIL_SOURCE = config('EMAIL_SOURCE')
# upload=multipart_threshold
    

#smtp settings

SENDER = 'info@dambaruu.com'  
SENDERNAME = 'SS Associates'
USERNAME_SMTP = "AKIA3L45B6NMEFUGVSGI"
PASSWORD_SMTP = "BNXeVpiDHPlV77Th+xMJPw0AlWzOfHcAnxGkFr+gWA+G"
EMAIL_HOST = "email-smtp.ap-south-1.amazonaws.com"
EMAIL_PORT = 587


#RAZORPAY CONFIGURATION

RAZOR_KEY_ID = "rzp_test_lmUi6exIAlVmDc"
RAZOR_KEY_SECRET = "Gw4y9DGD1RlVj1yWZxlv1eYc"
   

 
