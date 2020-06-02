from backend.settings.base import *

DEBUG = True
SECRET_KEY = "dev"

# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": os.path.join(BASE_DIR, "db.sqlite3"),
    }
}

TEST_RUNNER = "django_nose.NoseTestSuiteRunner"

NOSE_ARGS = [
    "--with-coverage",
    "--cover-package=backend",
    "--verbosity=2"
]

INSTALLED_APPS += [
    "django_nose"
]

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
