import pymysql

from encouragemint.settings.base import *

DEBUG = False

pymysql.version_info = (1, 3, 13, "final", 0)
pymysql.install_as_MySQLdb()

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": os.getenv("MYSQL_DATABASE"),
        "USER": os.getenv("MYSQL_USER"),
        "PASSWORD": os.getenv("MYSQL_PASSWORD"),
        "HOST": "db",
        "PORT": "3306"
    }
}

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_HOST_USER = "encouragemint.do.not.reply@gmail.com"
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_ACCOUNT_PASSWORD")
