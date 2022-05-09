from django.db import models

class BranchChief(models.Model):
    name = models.EmailField(max_length = 254)

class DirectSupervisor(models.Model):
    name = models.EmailField(max_length = 254) 