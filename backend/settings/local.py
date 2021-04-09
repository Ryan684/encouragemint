from backend.settings.base import *

DEBUG = True
SECRET_KEY = "dev"

TEST_RUNNER = "django_nose.NoseTestSuiteRunner"

NOSE_ARGS = [
    "--with-coverage",
    "--cover-package=backend",
    "--verbosity=2"
]

INSTALLED_APPS += [
    "django_nose"
]
