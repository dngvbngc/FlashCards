from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Set(models.Model):
    owner = models.ForeignKey("User", on_delete=models.CASCADE, related_name="sets")
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

class Card(models.Model):
    set = models.ForeignKey("Set", on_delete=models.CASCADE, related_name="cards")
    term = models.CharField(max_length=255)
    definition = models.TextField()