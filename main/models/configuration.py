from django.db import models

class Configuration(models.Model):
    length_of_reporting_cycle = models.CharField(max_length=20)
    