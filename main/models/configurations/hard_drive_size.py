from django.db import models

class HardDriveSize(models.Model):
    name = models.CharField(max_length=20)