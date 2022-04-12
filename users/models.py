from django.db import models
from django.contrib.auth.models import AbstractUser

class UserProfile(AbstractUser):
    class Status(models.TextChoices):
        PENDING = 'Pending'
        ACTIVE = 'Active'
        DISABLED = 'Disabled'
        ARCHIVED = 'Archived'

    direct_supervisor_email = models.EmailField()
    branch_chief_email = models.EmailField()
    status = models.CharField(max_length = 20, choices= Status.choices, default=Status.PENDING)
    last_modified_date = models.DateField(auto_now=True)
