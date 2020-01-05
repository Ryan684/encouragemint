import uuid

from django.db import models


class Profile(models.Model):
    profile_id = models.UUIDField(default=uuid.uuid4)
    first_name = models.CharField(max_length=25)
    last_name = models.CharField(max_length=25)


class Garden(models.Model):
    garden_id = models.UUIDField(default=uuid.uuid4)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="gardens")
    garden_name = models.CharField(max_length=25)
    direction = models.CharField(max_length=5)
    location = models.CharField(max_length=100)
    latitude = models.FloatField()
    longitude = models.FloatField()

    @property
    def sunlight(self):
        if self.direction == "north":
            return "low"
        if self.direction == "south":
            return "high"
        return "medium"


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
