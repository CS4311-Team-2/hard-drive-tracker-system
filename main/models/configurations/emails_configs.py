from django.db import models

class BranchChief(models.Model):
    name = models.CharField(max_length=20) 

class DirectSupervisor(models.Model):
    name = models.CharField(max_length=20)  