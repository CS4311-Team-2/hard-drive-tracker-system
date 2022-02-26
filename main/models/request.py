from datetime import datetime
from pickle import NONE
from django.db import models
from unixtimestampfield.fields import UnixTimeStampField

class Request(models.Model):

    class Request_Status(models.TextChoices):
        CREATED = "pending"
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
    
    request_reference_no = models.IntegerField()
    request_reference_no_year = UnixTimeStampField(auto_now_add=True)
    request_status = models.CharField(max_length = 50, choices= Request_Status.choices, default=Request_Status.CREATED)
    request_creation_date = UnixTimeStampField(auto_now_add=True)
    request_last_modifed_date = UnixTimeStampField(auto_now=True, blank=True)
    need_drive_by_date = models.CharField(max_length = 50)
    comment = models.TextField(blank = True) 
    file_attachment = models.FileField()
   
    class Meta:
        verbose_name_plural = "Request"
