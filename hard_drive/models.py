from email.policy import default
from django.db import models
from django.utils import timezone
from unixtimestampfield.fields import UnixTimeStampField


# Create your models here.

class HardDrive(models.Model):
    id = models.TextField(primary_key=True)
    # TODO: Make sure this field when the object is created. 
    create_date = UnixTimeStampField(auto_now_add=True) 
    manufacturer = models.TextField(blank=True, default='')
    hard_drive_type = models.TextField(blank=True, default='')
    connection_port = models.TextField(blank=True, default='')
    hard_drive_size = models.TextField(blank=True, default='')
    status = models.TextField(blank=True, default='')
    serial_number = models.TextField(blank=True, default='')
    classification = models.TextField(blank=True, default='')
    image_verion_id = models.TextField(blank=True, default='')
    boot_test_expiration = UnixTimeStampField(default=timezone.now)
    boot_test_status = models.TextField(blank=True, default='')
    justification_for_hard_drive_status_change = models.TextField(blank=True, default='')
    connection_port = models.TextField(blank=True, default='')
    issue_date = UnixTimeStampField(default=timezone.now)
    
    #TODO Need to add foreign key to request. 
