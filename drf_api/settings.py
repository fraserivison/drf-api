from pathlib import Path
import os
from dotenv import load_dotenv
import dj_database_url

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

# --------------------
# Basic settings
# --------------------
SECRET_KEY = os.environ.get("SECRET_KEY")
DEBUG = os.getenv("DEBUG", "True") == "True"

ALLOWED_HOSTS = [
    os.environ.get("ALLOWED_HOST"),
    "localhost",
    "8000-fraserivison-drfapi-d10c7zwdb71.ws-eu117.gitpod.io",
    "wave-drf-api-1157a4fa181b.herokuapp.com",
    "fraserivison.github.io",  # Added to allow GitHub Pages
]

# --------------------
# Database
# --------------------
DATABASE_URL = os.environ.get("DATABASE_URL")
DATABASES = {
    "default": dj_database_url.parse(DATABASE_URL, conn_max_age=600)
    if DATABASE_URL else {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# --------------------
# Installed apps
# --------------------
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "cloudinary_storage",
    "cloudinary",
    "rest_framework",
    "rest_framework_simplejwt",
    "django_filters",
    "rest_framework.authtoken",
    "dj_rest_auth",
    "django.contrib.sites",
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "dj_rest_auth.registration",
    "corsheaders",

    # Your apps
    "comments",
    "events",
    "followers",
    "profiles",
    "ratings",
    "tracks",
]
SITE_ID = 1

# --------------------
# Middleware
# --------------------
MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",  # Keep CORS middleware at the top
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "allauth.account.middleware.AccountMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# --------------------
# REST Framework & Auth
# --------------------
REST_USE_JWT = True
REST_AUTH_SERIALIZERS = {
    "USER_DETAILS_SERIALIZER": "drf_api.serializers.CurrentUserSerializer"
}

if DEBUG:
    DEFAULT_AUTH_CLASS = "rest_framework.authentication.SessionAuthentication"
    JWT_AUTH_SECURE = False
    JWT_AUTH_SAMESITE = "Lax"
else:
    DEFAULT_AUTH_CLASS = "dj_rest_auth.jwt_auth.JWTCookieAuthentication"
    JWT_AUTH_SECURE = True
    JWT_AUTH_SAMESITE = "None"

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [DEFAULT_AUTH_CLASS],
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 12,
    "DATETIME_FORMAT": "%d %b %Y",
}

if not DEBUG:
    REST_FRAMEWORK["DEFAULT_RENDERER_CLASSES"] = ["rest_framework.renderers.JSONRenderer"]

JWT_AUTH_COOKIE = "my-access-token"
JWT_AUTH_REFRESH_COOKIE = "my-refresh-token"
JWT_AUTH_HTTPONLY = True  # Keep JWT cookie HttpOnly for security

# --------------------
# Allauth settings
# --------------------
ACCOUNT_SIGNUP_FIELDS = ["username*", "password1*"]
ACCOUNT_EMAIL_VERIFICATION = "none"
ACCOUNT_LOGIN_METHODS = {"username"}

AUTHENTICATION_BACKENDS = (
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
)

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

# --------------------
# CORS / CSRF
# --------------------
CORS_ALLOW_ALL_ORIGINS = False  # Turn off in favor of explicit origins
CORS_ALLOW_CREDENTIALS = True  # Allow cookies to be sent cross-site
CORS_ALLOW_HEADERS = ["Authorization", "Content-Type"]
CORS_ALLOW_METHODS = ["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"]

CORS_ALLOWED_ORIGINS = [
    "https://3000-fraserivison-waveapp-f3at7xflsi4.ws-eu117.gitpod.io",
    "http://localhost:3000",
    "https://wave-drf-api-1157a4fa181b.herokuapp.com",
    "https://fraserivison.github.io",  # Added for GitHub Pages
]

CSRF_TRUSTED_ORIGINS = [
    "https://wave-app-b7b6d5495ba9.herokuapp.com",
    "https://3000-fraserivison-waveapp-f3at7xflsi4.ws-eu117.gitpod.io",
    "https://8000-fraserivison-drfapi-d10c7zwdb71.ws-eu117.gitpod.io",
    "https://wave-drf-api-1157a4fa181b.herokuapp.com",
    "https://fraserivison.github.io",  # Added for GitHub Pages
]

CSRF_COOKIE_SAMESITE = "None"  # Needed for cross-site cookies
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SAMESITE = "None"  # Needed for cross-site cookies
SESSION_COOKIE_SECURE = True

# --------------------
# Templates, WSGI, etc
# --------------------
ROOT_URLCONF = "drf_api.urls"
WSGI_APPLICATION = "drf_api.wsgi.application"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
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

# --------------------
# Password validation
# --------------------
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# --------------------
# Internationalization
# --------------------
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_L10N = True
USE_TZ = True

# --------------------
# Static files
# --------------------
STATIC_URL = "/static/"
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
