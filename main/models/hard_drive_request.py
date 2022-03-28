from django.db import models
from main.models.hard_drive import HardDrive
from main.models.request import Request
from unixtimestampfield.fields import UnixTimeStampField
from email.policy import default
from django.db import models

# Hard Drive request model
class HardDriveRequest(models.Model):
    classification = models.CharField(max_length=50, choices=HardDrive.Classification.choices, 
                                        default=HardDrive.Classification.UNCLASSIFIED)
    amount_required = models.IntegerField(default=1) 
    connection_port = models.CharField(
        max_length=50,
        choices = HardDrive.ConnectionPort.choices,
        default = HardDrive.ConnectionPort.M2)
    hard_drive_size = models.CharField(max_length=50,blank=True)
    hard_drive_type = models.CharField(max_length=20)
    comment = models.TextField(blank=True)
    request = models.ForeignKey(
        Request,
        on_delete=models.CASCADE,
        blank=True, null=True, 
        related_name="hard_drive_requests")

    class Meta:
        verbose_name_plural = "Hard Drive Request"