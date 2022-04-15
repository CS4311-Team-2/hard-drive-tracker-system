from urllib import request
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from main.filters import UserProfilesFilter
from users.models import UserProfile


from main.forms import HardDriveConnectionPortsForm, HardDriveTypeForm, HardDriveManufacturersForm
from main.views.decorators import group_required
from main.models.hard_drive import HardDrive
from main.models.request import Request
from main.models.event import Event
from main.models.log import Log
from main.models.configurations.hard_drive_connection_ports import HardDriveConnectionPorts
from main.forms import HardDriveForm
from main.models.configurations.hard_drive_type import HardDriveType
from main.models.configurations.hard_drive_manufacturers import HardDriveManufacturers




@login_required(login_url='main:login')
@group_required('Administrator')
def view_all_profiles(request):
    userProfiles = UserProfile.objects.all()

    profileFilter = UserProfilesFilter(request.GET, queryset=userProfiles)
    userProfiles = profileFilter.qs

    context = {"userProfiles" : userProfiles, "profileFilter" : profileFilter}
    return render(request, 'maintainer/view_all_profiles.html', context)