import uuid

from django.db import models


class Profile(models.Model):
    profile_id = models.UUIDField(default=uuid.uuid4)
    first_name = models.CharField(max_length=25)
    last_name = models.CharField(max_length=25)


class Plant(models.Model):
    plant_id = models.ForeignKey(Profile, on_delete=models.CASCADE)
    plant_name = models.CharField(max_length=25)