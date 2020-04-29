import logging

from encouragemint.celery import app
from encouragemint.encouragemint.exceptions import GardenUserError, GardenSystemError
from encouragemint.encouragemint.garden_locator import register_garden_coordinates

logger = logging.getLogger("django")


@app.task(bind=True, autoretry_for=(GardenSystemError,), retry_backoff=True, max_retries=None)
def add_garden_location(self, garden_id):  # pylint: disable=unused-argument
    try:
        register_garden_coordinates(garden_id)
    except (GardenSystemError, GardenUserError) as exception:
        logger.error(exception)
        raise
