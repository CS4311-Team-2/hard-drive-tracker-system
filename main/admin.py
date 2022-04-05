
from django.contrib import admin

from main.models.configurations.hard_drive_type import HardDriveType
from main.models.hard_drive import HardDrive
from main.models.event import Event
from main.models.request import Request
from main.models.hard_drive_request import HardDriveRequest


admin.site.register(HardDrive)
admin.site.register(Request)
admin.site.register(HardDriveRequest)
admin.site.register(Event)
admin.site.register(HardDriveType)
