from datetime import datetime
from django.db import models
from unixtimestampfield.fields import UnixTimeStampField

from main.models.request import Request

class Event(models.Model):
    class Status(models.TextChoices):
        CONFIRMED = "confirmed"
        FORECASTED = "forecasted"
        CANCELED = "canceled"
    
    event_name = models.TextField(blank = True)
    event_description = models.TextField(blank= True)
    event_location = models.TextField(blank = True)
    event_type = models.TextField(blank = True)
    length_of_reporting_cycle = UnixTimeStampField(blank = True)
    event_status = models.CharField(max_length=50, choices = Status.choices, default = Status.CONFIRMED)
    event_start_date = UnixTimeStampField(blank = True)
    event_end_date = UnixTimeStampField(blank = True)
    event = models.ForeignKey(Request, on_delete=models.CASCADE, blank=True, null=True, related_name="event")

    class Meta:
        verbose_name_plural = "Event"