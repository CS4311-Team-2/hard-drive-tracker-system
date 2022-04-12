from django.db import models

class HardDriveConnectionPorts(models.Model):
    name = models.CharField(max_length=20)    