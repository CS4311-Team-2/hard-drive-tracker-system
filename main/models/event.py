from datetime import datetime
from django.db import models
from unixtimestampfield.fields import UnixTimeStampField

from main.models.request import Request

# Event model
class Event(models.Model):
    class Status(models.TextChoices):
        CONFIRMED = "confirmed"
        FORECASTED = "forecasted"
        CANCELED = "canceled"

    class Type(models.TextChoices):
        PMR = "PMR"
        CVPA = "CVPA"
        CVI = "CVI"
        VOF = "VoF"
        CR = "Cyber Resilience"
        IP = "Individual Project"
        RP = "Research Project"

    
    event_name = models.CharField(max_length=100, blank = True)
    event_description = models.TextField(blank= True)
    event_location = models.CharField(max_length=100, blank = True)
    event_type = models.CharField(max_length=50, choices = Type.choices, default = Type.PMR)
    length_of_reporting_cycle = models.TextField(blank = True)
    event_status = models.CharField(max_length=50, choices = Status.choices, default = Status.CONFIRMED)
    event_start_date = models.DateField(auto_now=False, auto_now_add=False)
    event_end_date = models.DateField(blank = True)
    request = models.ForeignKey(Request, on_delete=models.CASCADE, blank=True, null=True, related_name="event")

    class Meta:
        verbose_name_plural = "Event"