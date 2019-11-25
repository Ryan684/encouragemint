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
    plant_name = models.CharField(max_length=25)
