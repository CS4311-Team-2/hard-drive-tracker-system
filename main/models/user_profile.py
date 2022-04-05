from django.db import models

class UserProfile(models.Model):
   gender = models.BooleanField(default=True)