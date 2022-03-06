from django.contrib import admin
from .models import HardDrive, Request, HardDriveRequest


admin.site.register(HardDrive)
admin.site.register(Request)
admin.site.register(HardDriveRequest)