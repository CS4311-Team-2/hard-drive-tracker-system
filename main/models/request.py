from datetime import datetime
from email.policy import default
from django.db import models

class Request(models.Model):
    #class Request_Reference_No(models.Field):
    #    year = datetime.year
    #     referece_no = models.DecimalField(decimal_places = 0, max_digits= 4)
    

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
    
    #request_reference_no = models.CharField(Request_Reference_No())
    request_status = models.CharField(max_length = 50, choice= Request_status)
    request_creation_date = models.DateTimeField(auto_now_add=True)
    request_last_modifed_date = models.DateTimeField(auto_now=True, blank=True)
    need_drive_by_date = models.DateField() 
    comment = models.TextField(blank = True)  
   
    class Meta:
        verbose_name_plural = "Request"
