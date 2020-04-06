import logging

from encouragemint.celery import app
from encouragemint.encouragemint.exceptions import GardenUserError, GardenSystemError
from encouragemint.encouragemint.garden import create_garden

logger = logging.getLogger("django")


@app.task(bind=True, autoretry_for=(GardenSystemError,), retry_backoff=True, max_retries=None)
def add_garden(self, garden_data):
    try:
        return create_garden(garden_data)
    except (GardenSystemError, GardenUserError) as exception:
        logger.error(exception)
        raise
