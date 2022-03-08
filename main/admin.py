from django.contrib import admin
from .models import HardDrive, Request, HardDriveRequest, Event


admin.site.register(HardDrive)
admin.site.register(Request)
admin.site.register(HardDriveRequest)
admin.site.register(Event)