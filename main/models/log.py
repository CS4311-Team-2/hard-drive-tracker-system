from datetime import datetime
from django.db import models
from unixtimestampfield.fields import UnixTimeStampField
import time 
from main.models.request import Request

# Log model
class Log(models.Model):
    time_stamp = models.DateTimeField(auto_now_add=True)
    #user = models.CharField(max_length = 50)
    action_preformed = models.CharField(max_length = 500)


