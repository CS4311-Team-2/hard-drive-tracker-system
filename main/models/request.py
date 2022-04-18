from django.db import models
from django.conf import settings

# Request model
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
    
    request_reference_no = models.AutoField(primary_key=True)
    request_reference_no_year = models.DateField(blank=True)
    request_status = models.CharField(max_length=50, choices=Request_Status.choices, 
                                        default=Request_Status.CREATED)
    request_creation_date = models.DateField(auto_now_add=True)
    request_last_modifed_date = models.DateField(auto_now=True,blank=True)
    need_drive_by_date = models.DateField(max_length=50,blank=True)
    comment = models.TextField(blank = True) 
    user = models.ForeignKey(settings.AUTH_USER_MODEL, default=1, on_delete=models.CASCADE)
   
    class Meta:
        verbose_name_plural = "Request"

