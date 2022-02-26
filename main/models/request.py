<<<<<<< HEAD
from datetime import datetime
from pickle import NONE
=======
>>>>>>> 61eb28123693bab9010058e3376e15847032a2fa
from django.db import models
from unixtimestampfield.fields import UnixTimeStampField
from email.policy import default
from django.db import models

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
    
<<<<<<< HEAD
    request_reference_no = models.IntegerField()
    request_reference_no_year = UnixTimeStampField(auto_now_add=True)
    request_status = models.CharField(max_length = 50, choices= Request_Status.choices, default=Request_Status.CREATED)
    request_creation_date = UnixTimeStampField(auto_now_add=True)
    request_last_modifed_date = UnixTimeStampField(auto_now=True, blank=True)
=======
    request_reference_no = models.CharField(primary_key=True, max_length=50)
    request_reference_no_year = UnixTimeStampField(use_numeric=True, auto_now_add=True,default=0.0)
    request_status = models.CharField(max_length = 50, choices= Request_Status.choices)
    request_creation_date = UnixTimeStampField(use_numeric=True, auto_now_add=True,default=0.0)
    request_last_modifed_date = UnixTimeStampField(use_numeric=True, auto_now=True,default=0.0)
>>>>>>> 61eb28123693bab9010058e3376e15847032a2fa
    need_drive_by_date = models.CharField(max_length = 50)
    comment = models.TextField(blank = True) 
    #file_attachment = models.FileField()
   
    class Meta:
        verbose_name_plural = "Request"


class HardDriveRequest(models.Model):

    class Classification(models.TextChoices):
        CLASSIFIED = "classified"
        UNCLASSIFIED = "unclassified"

    # key to the hard drive. 
    classification = models.CharField(max_length=50, choices=Classification.choices, 
                                        default=Classification.UNCLASSIFIED)
    amount_required = models.IntegerField(default=1) 
    connection_port = models.CharField(max_length=50, default='SATA')
    hard_drive_size = models.CharField(max_length=50,blank=True)
    hard_drive_type = models.CharField(max_length=50,blank=True)
    comment = models.TextField(blank=True)
    request = models.ForeignKey(Request, 
                on_delete=models.CASCADE, blank=True, null=True, related_name="hard_drive_requests")

    class Meta:
        verbose_name_plural = "Hard Drive Request"