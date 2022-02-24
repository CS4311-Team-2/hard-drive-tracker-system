from datetime import datetime
from django.db import models
from unixtimestampfield.fields import UnixTimeStampField
from django import forms

class Request(models.Model):
    
    class UploadFileForm(forms.Form):
        title = forms.CharField(max_length=50)
        file = forms.FileField()

    class Request_status(models.TextChoices):
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
    
    request_reference_no = models.IntegerField()
    request_reference_no_year = UnixTimeStampField(auto_now_add=True)
    request_status = models.CharField(max_length = 50, choice= Request_status)
    request_creation_date = models. UnixTimeStampField(auto_now_add=True)
    request_last_modifed_date = models. UnixTimeStampField(auto_now=True, blank=True)
    need_drive_by_date = models.CharField(max_length = 50)
    comment = models.TextField(blank = True) 
    file_attachment = models.FileField()
   
    class Meta:
        db_table = "Request"
