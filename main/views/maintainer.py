from urllib import request
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required

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

# These functions relate to maintainer/*.html views. These functions serve only the 
#   maintainer role. 

@login_required(login_url='main:login')
@group_required('Maintainer')
def home(request):
    requests = Request.objects.filter(request_status = Request.Request_Status.CREATED)
    overdue_requests = Request.objects.filter(request_status = Request.Request_Status.OVERDUE)
    deliquentdrives = HardDrive.objects.filter(request__in = overdue_requests)

    context = {
        "deliquentdrives" : deliquentdrives, 
        "requests" : requests,
    }
    return render(request, 'maintainer/home.html', context)

@login_required(login_url='main:login')
@group_required('Maintainer')
def view_request(request):
    return render(request, 'maintainer/view_request.html')

@login_required(login_url='main:login')
@group_required('Maintainer')
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
@group_required('Maintainer')
def view_all_harddrives(request):
    hardDrives = HardDrive.objects.all()

    context = {"hardDrives" : hardDrives}
    return render(request, 'maintainer/view_all_hard_drives.html', context)

@login_required(login_url='main:login')
@group_required('Maintainer')
def add_hard_drive(http_request):
    form = HardDriveForm()
    if (http_request.method == 'POST'):
        form = HardDriveForm(http_request.POST)
        if form.is_valid():
            hard_drive = form.save(commit=False)
            hard_drive.modifier = http_request.user
            hard_drive.save()
            Log.objects.create(action_performed="Created the hard drive: " + hard_drive.serial_number, user=http_request.user)
            return redirect('main:index')
        else:
            print(form.errors)
    return render(http_request, 'maintainer/view_hard_drive.html', {'form': form, VIEW_HARD_DRIVE:False}) 

@login_required(login_url='main:login')
@group_required('Maintainer')
def view_hard_drive(http_request, id=-1):
    if id==-1:
        print("ERROR ERROR")    
    hard_drive = HardDrive.objects.filter(pk=id).first()
    modifier = hard_drive.modifier.email

    # Saves new hard drive. 
    if http_request.method == 'POST':
        form = HardDriveForm(http_request.POST, instance=hard_drive)
        if form.is_valid():
            hard_drive = form.save(commit=False)
            hard_drive.modifier = http_request.user
            hard_drive.save()
            Log.objects.create(action_performed="Modified the hard drive: " + hard_drive.serial_number, user=http_request.user)
        else:
            print(form.errors)
    else:
        form = HardDriveForm(instance=hard_drive)
        form['modifier'].initial = modifier
    return render(http_request, 'maintainer/view_hard_drive.html', {"form" : form, 'id':id, 'email':hard_drive.modifier.email, VIEW_HARD_DRIVE:True})

@login_required(login_url='main:login')
@group_required('Maintainer')
def configuration(request):    
    hard_drive_types = HardDriveType.objects.all()
    hard_drive_manufacturers = HardDriveManufacturers.objects.all()
    hard_drive_connection_ports = HardDriveConnectionPorts.objects.all()
    context = {
        "hard_drive_types" : hard_drive_types,
        "hard_drive_types_form" : HardDriveTypeForm(),
        "hard_drive_manufacturers": hard_drive_manufacturers,
        "hard_drive_manufacturers_form": HardDriveManufacturersForm(),
        "hard_drive_connection_ports": hard_drive_connection_ports,
        "hard_drive_connection_port_form": HardDriveConnectionPortsForm()
        }
    return render(request, 'maintainer/configuration.html', context)

@login_required(login_url='main:login')
@group_required('Maintainer')
def view_log(request):
    logs = Log.objects.all()
    context = {"Logs" : logs}
    return render(request, 'log/view_log.html', context)

