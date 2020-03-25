import uuid

from django.db import models

from encouragemint.encouragemint.models.garden import Garden


class Plant(models.Model):
    plant_id = models.UUIDField(default=uuid.uuid4)
    garden = models.ForeignKey(Garden, on_delete=models.CASCADE, related_name="plants")
    common_name = models.CharField(max_length=50)
    trefle_id = models.IntegerField()
    scientific_name = models.CharField(max_length=50)
    duration = models.CharField(max_length=25, null=True)
    bloom_period = models.CharField(max_length=25, null=True)
    growth_period = models.CharField(max_length=25, null=True)
    growth_rate = models.CharField(max_length=25, null=True)
    shade_tolerance = models.CharField(max_length=25, null=True)
    moisture_use = models.CharField(max_length=25, null=True)
    family_common_name = models.CharField(max_length=50)