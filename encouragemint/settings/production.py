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
