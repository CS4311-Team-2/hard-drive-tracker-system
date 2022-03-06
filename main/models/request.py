from django.db import models
from django.conf import settings

from unixtimestampfield.fields import UnixTimeStampField

class Request(models.Model):

    class Request_Status(models.TextChoices):
        CREATED = "created"
        FORECASTED = "forecasted"
        CONFIRMED = "confirmed"
        APPROVED = "approved"
        DECLINED = "declined"
        DELIVERED = "delivered"
        FULLFILLED = "fullfilled"
        PARTIAL_RETURNED = "partial-returned"
        CLOSED = "closed"
        CANCELED = "cancelled"
        ARCHIVED = "archived"
        OVERDUE = "overdue"
    #Forecasted, confirmed shall be constrained by event status.?
    
    request_reference_no = models.CharField(primary_key=True, max_length=50)
    request_reference_no_year = UnixTimeStampField(use_numeric=True, auto_now_add=True,default=0.0)
    request_status = models.CharField(max_length = 50, choices= Request_Status.choices, default=Request_Status.CREATED)
    request_creation_date = UnixTimeStampField(use_numeric=True, auto_now_add=True,default=0.0)
    request_last_modifed_date = UnixTimeStampField(use_numeric=True, auto_now=True,default=0.0)
    need_drive_by_date = models.CharField(max_length = 50)
    comment = models.TextField(blank = True) 
    user = models.ForeignKey(settings.AUTH_USER_MODEL, default=1, on_delete=models.CASCADE)
    #file_attachment = models.FileField()
   
    class Meta:
        verbose_name_plural = "Request"

