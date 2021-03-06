from django.db import models
from django.conf import settings
from .request import Request

class Amendment(models.Model):
    class Status(models.TextChoices):
        PENDING = 'pending'
        APPROVED = 'approved'
        DENIED = 'denied'

    created = models.DateField(auto_now_add=True)
    description  = models.TextField(blank=True)
    decision_date = models.DateField(blank=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    comment = models.TextField(blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,default=1,
                                on_delete=models.CASCADE)
    request = models.ForeignKey(Request, on_delete=models.CASCADE, null=True,
                                    blank=True, related_name='admendments')
