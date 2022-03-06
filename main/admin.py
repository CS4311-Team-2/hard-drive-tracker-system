from django.contrib import admin
from .models import Listings, HardDrive, Request, HardDriveRequest, Event


admin.site.register(Listings)
admin.site.register(HardDrive)
admin.site.register(Request)
admin.site.register(HardDriveRequest)
admin.site.register(Event)