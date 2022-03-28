from django.db import models

class EventType(models.Model):
    name = models.CharField(max_length=20)