from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required

from main.forms import HardDriveTypeForm, HardDriveManufacturersForm, HardDriveConnectionPortsForm, HardDriveSizeForm, EventForm, RequestForm
from main.views.decorators import group_required
from main.models.configurations.hard_drive_type import HardDriveType
from main.models.configurations.hard_drive_manufacturers import HardDriveManufacturers
from main.models.configurations.hard_drive_connection_ports import HardDriveConnectionPorts
from main.models.configurations.hard_drive_size import HardDriveSize
from main.models.hard_drive import HardDrive
from main.models.request import Request
from main.models.event import Event
from main.models.hard_drive_request import HardDriveRequest
from main.views.maintainer import get_request_form

@login_required(login_url='main:login')
@group_required('Maintainer')
def hard_drive_type(request):
    print("----------\nHard Drive Type\n-------")
    form = HardDriveTypeForm(request.POST)
    if form.is_valid():
        form.save()
    hard_drive_types = HardDriveType.objects.all()
    context = {"hard_drive_types" : hard_drive_types,}
    return render(request, 'components/hard_drive_types.html', context)

@login_required(login_url='main:login')
@group_required('Maintainer')
def delete_hard_drive_type(request, pk):
    HardDriveType.objects.get(pk = pk).delete()
    hard_drive_types = HardDriveType.objects.all()
    context = {
        "hard_drive_types" : hard_drive_types,
    }
    return render(request, 'components/hard_drive_types.html', context)

@login_required(login_url='main:login')
@group_required('Maintainer')
def hard_drive_manufacturer(request):
    print("----------\nHard Drive Manufacturer\n-------")
    form =  HardDriveManufacturersForm(request.POST)
    if form.is_valid():
        form.save()
    hard_drive_manufacturers = HardDriveManufacturers.objects.all()
    context = {"hard_drive_manufacturers" : hard_drive_manufacturers,}
    return render(request, 'components/hard_drive_manufacturers.html', context)

@login_required(login_url='main:login')
@group_required('Maintainer')
def delete_hard_drive_manufacturer(request, pk):
    HardDriveManufacturers.objects.get(pk = pk).delete()
    hard_drive_manufacturers = HardDriveManufacturers.objects.all()
    context = {
        "hard_drive_manufacturers" : hard_drive_manufacturers,
    }
    return render(request, 'components/hard_drive_manufacturers.html', context)

@login_required(login_url='main:login')
@group_required('Maintainer')
def hard_drive_connection_port(request):
    print("----------\nHard Drive Connection Port\n-------")
    form =  HardDriveConnectionPortsForm(request.POST)
    if form.is_valid():
        form.save()
    hard_drive_connection_port = HardDriveConnectionPorts.objects.all()
    context = {"hard_drive_connection_ports" : hard_drive_connection_port,}
    return render(request, 'components/hard_drive_connection_port.html', context)

@login_required(login_url='main:login')
@group_required('Maintainer')
def delete_hard_drive_connection_port(request, pk):
    HardDriveConnectionPorts.objects.get(pk = pk).delete()
    hard_drive_connection_port = HardDriveConnectionPorts.objects.all()
    context = {
        "hard_drive_connection_ports" : hard_drive_connection_port,
    }
    return render(request, 'components/hard_drive_connection_port.html', context)


@login_required(login_url='main:login')
@group_required('Maintainer')
def hard_drive_size(request):
    print("----------\nHard Drive Size\n-------")
    form =  HardDriveSizeForm(request.POST)
    if form.is_valid():
        form.save()
    hard_drive_size = HardDriveSize.objects.all()
    context = {"hard_drive_size" : hard_drive_size,}
    return render(request, 'components/hard_drive_size.html', context)

@login_required(login_url='main:login')
@group_required('Maintainer')
def delete_hard_drive_size(request, pk):
    HardDriveSize.objects.get(pk = pk).delete()
    hard_drive_size = HardDriveSize.objects.all()
    context = {
        "hard_drive_size" : hard_drive_size,
    }
    return render(request, 'components/hard_drive_size.html', context)

@login_required(login_url='main:login')
@group_required('Maintainer')
def assign_hard_drive(http_request):
    request = Request.objects.get(pk = http_request.POST['request_id'])
    print('serial-number:', http_request.POST['serial-number'])
    assigned_hard_drive = HardDrive.objects.get(serial_number = http_request.POST['serial-number'])
    print('assigned_hard_drive:', assigned_hard_drive)
    assigned_hard_drive.request = request
    assigned_hard_drive.status = HardDrive.Status.ASSIGNED
    
    assigned_hard_drive.save()
    request.save()
    assigned_hard_drives = HardDrive.objects.filter(request = request)

    context = {
        "req" : request,
        "hard_drives" : assigned_hard_drives,
    }
    return render(http_request, 'components/assigned_hard_drives.html', context)

@login_required(login_url='main:login')
@group_required('Maintainer')
def approve_request(http_request):
    req = Request.objects.get(pk = http_request.POST['request_id'])
    req.request_status = Request.Request_Status.APPROVED
    req.save()

    # used for event information
    event = Event.objects.filter(request = req).first()
    event_form = EventForm(instance=event)
    event_form.make_all_readonly()
    
    #used for assigned hard drive sections
    hard_drives = HardDrive.objects.filter(request = req)
    print(hard_drives)
    
    #used for the selecting hard drive section
    all_hard_drives = HardDrive.objects.filter(request = None)
    
    #used for requested hard drive
    requested_hard_drives = HardDriveRequest.objects.filter(request = req)
    request_form = RequestForm(instance=req)
    request_form = get_request_form(req)
    request_form.make_all_readonly()

    context = {
        'req' : req, 
        'request_form': request_form, 
        'event' :event_form, 
        'hard_drives' :hard_drives, 
        'all_hard_drives' : all_hard_drives, 
        'requested_hard_drives' : requested_hard_drives }
    return render(http_request, 'components/request.html', context)

@login_required(login_url='main:login')
@group_required('Maintainer')
def fulfill_request(http_request):
    req = Request.objects.get(pk = http_request.POST['request_id'])
    req.request_status = Request.Request_Status.FULLFILLED
    req.save()

    # used for event information
    event = Event.objects.filter(request = req).first()
    event_form = EventForm(instance=event)
    event_form.make_all_readonly()
    
    #used for assigned hard drive sections
    hard_drives = HardDrive.objects.filter(request = req)
    print(hard_drives)
    
    #used for the selecting hard drive section
    all_hard_drives = HardDrive.objects.filter(request = None)
    
    #used for requested hard drive
    requested_hard_drives = HardDriveRequest.objects.filter(request = req)
    request_form = RequestForm(instance=req)
    request_form = get_request_form(req)
    request_form.make_all_readonly()

    context = {
        'req' : req, 
        'request_form': request_form, 
        'event' :event_form, 
        'hard_drives' :hard_drives, 
        'all_hard_drives' : all_hard_drives, 
        'requested_hard_drives' : requested_hard_drives }
    return render(http_request, 'components/request.html', context)
