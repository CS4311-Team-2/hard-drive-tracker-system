from urllib import request
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import UserProfile


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

VIEW_HARD_DRIVE = "view_hard_drive"

# These functions relate to auditor/*.html views. These functions serve only the 
#   maintainer role. 

@login_required(login_url='main:login')
@group_required('Auditor')
def home(request):
    requests = Request.objects.filter(request_status = Request.Request_Status.CREATED)
    overdue_requests = Request.objects.filter(request_status = Request.Request_Status.OVERDUE)
    deliquent_drives = HardDrive.objects.none()
    for r in overdue_requests:
        deliquent_drives |= HardDrive.objects.filter(request=r)

    context = {
        "deliquent_drives" : deliquent_drives, 
        "requests" : requests,
    }
    return render(request, 'maintainer/home.html', context)

@login_required(login_url='main:login')
def audi_view_all_users(request):
    users_list = UserProfile.objects.all()
    context = {'users_lists' : users_list}
    return render(request, 'auditor/view_all_users.html', context=context)


@login_required(login_url='main:login')
@group_required('Auditor')
def view_all_requests(http_request):
    data = {}
    requests = Request.objects.all()
    for r in requests:
        events = Event.objects.filter(request = r)
        if not events:
            continue
        else:
            event = events[0]
        data[r] = event

    context = {'data': data, 'requests' : requests}
    return render(http_request, 'maintainer/view_all_requests.html', context)

@login_required(login_url='main:login')
@group_required('Auditor')
def view_all_harddrives(request):
    hardDrives = HardDrive.objects.all()

    context = {"hardDrives" : hardDrives}
    return render(request, 'maintainer/view_all_hard_drives.html', context)


