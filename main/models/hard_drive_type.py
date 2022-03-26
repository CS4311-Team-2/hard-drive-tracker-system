from django.db import models

class HardDriveType(models.Model):
    name = models.CharField(max_length=20)    