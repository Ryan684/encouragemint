import uuid

from django.contrib.auth.models import User
from django.db import models


class Garden(models.Model):
    garden_id = models.UUIDField(default=uuid.uuid4)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="gardens")
    garden_name = models.CharField(max_length=25)
    direction = models.CharField(max_length=5)
    location = models.CharField(max_length=100)
    latitude = models.FloatField(null=True)
    longitude = models.FloatField(null=True)

    @property
    def sunlight(self):
        if self.direction == "north":
            return "low"
        if self.direction == "south":
            return "high"
        return "medium"

    @property
    def shade_tolerance(self):
        if self.sunlight == "north":
            return "Tolerant"
        if self.sunlight == "south":
            return "Intolerant"
        return "Intermediate"
