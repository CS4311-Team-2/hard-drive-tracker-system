from django.db import models
from .models import HardDrive

# Create your models here.

class HardDrive(models.Model):
    id = models.TextField(primary_key=True)
    #TODO Need to add foreign key to request. 

