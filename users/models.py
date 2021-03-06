from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

class UserProfile(AbstractUser):

    class MockGroupIs(models.TextChoices):
        MAINTAINER = 'Maintainer'
        REQUESTOR = 'Requestor'

    class Status(models.TextChoices):
        PENDING = 'Pending'
        ACTIVE = 'Active'
        DISABLED = 'Disabled'
        ARCHIVED = 'Archived'

    direct_supervisor_email = models.EmailField()
    branch_chief_email = models.EmailField()
    status = models.CharField(max_length = 20, choices= Status.choices, default=Status.PENDING)
    last_modified_date = models.DateField(default=timezone.now, blank=True)

    # DEPRICATED 
    mock_group_is = models.CharField(max_length=20, choices=MockGroupIs.choices, default=MockGroupIs.MAINTAINER)