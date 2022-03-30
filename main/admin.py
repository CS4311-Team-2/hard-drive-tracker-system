from django.contrib import admin

from main.models.hard_drive_type import HardDriveType
from .models import HardDrive, Request, HardDriveRequest, Event

# Models that can be edited in admin page. 
admin.site.register(HardDrive)
admin.site.register(Request)
admin.site.register(HardDriveRequest)
admin.site.register(Event)
admin.site.register(HardDriveType)