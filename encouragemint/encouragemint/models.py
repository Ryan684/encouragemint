import uuid

from django.db import models


class Profile(models.Model):
    profile_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    first_name = models.CharField(max_length=25)
    last_name = models.CharField(max_length=25)


class Garden(models.Model):
    garden_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    garden_name = models.CharField(max_length=25)


class Plant(models.Model):
    plant_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    garden = models.ForeignKey(Garden, on_delete=models.CASCADE)
    scientific_name = models.CharField(max_length=25)
    duration = models.CharField(max_length=25, blank=True, null=True)
    bloom_period = models.CharField(max_length=25, blank=True, null=True)
    growth_period = models.CharField(max_length=25, blank=True, null=True)
    growth_rate = models.CharField(max_length=25, blank=True, null=True)
    shade_tolerance = models.CharField(max_length=25, blank=True, null=True)
    moisture_use = models.CharField(max_length=25, blank=True, null=True)
    family_name = models.CharField(max_length=25)
