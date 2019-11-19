from encouragemint.settings.base import *

TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'

NOSE_ARGS = [
    '--with-coverage',
    '--cover-package=encouragemint',
    '--verbosity=2'
]

INSTALLED_APPS += [
    'django_nose'
]