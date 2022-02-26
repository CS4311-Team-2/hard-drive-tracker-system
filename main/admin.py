from django.contrib import admin

from main.models.request import Request
from .models import Listings, HardDrive


admin.site.register(Listings)
admin.site.register(HardDrive)
admin.site.register(Request)