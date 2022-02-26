from django.db import models
from unixtimestampfield.fields import UnixTimeStampField
from email.policy import default
from django.db import models
from request import Request

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
    request = models.ForeignKey(Request, on_delete=models.CASCADE, blank=True, null=True, related_name="hard_drive_requests")

    class Meta:
        verbose_name_plural = "Hard Drive Request"