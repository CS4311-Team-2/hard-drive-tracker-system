from django.contrib import admin
from .models import HardDrive, Request, HardDriveRequest, Event

# Models that can be edited in admin page. 
admin.site.register(HardDrive)
admin.site.register(Request)
admin.site.register(HardDriveRequest)
admin.site.register(Event)