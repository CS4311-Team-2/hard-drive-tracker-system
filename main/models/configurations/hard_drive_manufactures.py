from django.db import models

class HardDriveManufactures(models.Model):
    name = models.CharField(max_length=20)    