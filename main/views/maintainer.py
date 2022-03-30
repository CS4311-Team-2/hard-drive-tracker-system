from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.core.management import call_command
from django.forms.models import modelformset_factory


from datetime import datetime
from main.forms import HardDriveTypeForm
from main.models import hard_drive_type

from main.views.decorators import group_required
from main.models.hard_drive import HardDrive
from main.models.request import Request
from main.models.event import Event
from main.forms import HardDriveForm
from main.models.hard_drive_type import HardDriveType
from django import db

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
def add_hard_drive(http_request):
    
    if (http_request.method == 'POST'):
        data = dict(http_request.POST)
        form = HardDriveForm(http_request.POST)
        if form.is_valid():
            hard_drive = form.save()
            return redirect('main:index')
        else:
            print(form.errors)
    else:
        print('groups:', http_request.user.groups)
        return render(http_request, 'maintainer/add_hard_drive.html', {'form': HardDriveForm()})

@login_required(login_url='main:login')
@group_required('Maintainer')
def view_all_harddrives(request):
    hardDrives = HardDrive.objects.all()

    context = {"hardDrives" : hardDrives}
    return render(request, 'maintainer/view_all_hard_drives.html', context)

@login_required(login_url='main:login')
@group_required('Maintainer')
def view_hard_drive(http_request, id=-1):
    if id==-1:
        print("ERROR ERROR")    
    hard_drive = HardDrive.objects.filter(pk=id).first()

    # Saves new hard drive. 
    if http_request.method == 'POST':
        form = HardDriveForm(http_request.POST, instance=hard_drive)
        if form.is_valid():
            form.save()
            return render(http_request, 'maintainer/view_hard_drive.html', {'form': form, 'id':form})
        else:
            print(form.errors)
            
    else:
        form = HardDriveForm(instance=hard_drive)
    
    return render(http_request, 'maintainer/view_hard_drive.html', {"form" : form, 'id':id})

@login_required(login_url='main:login')
@group_required('Maintainer')
def configuration(request):
    form = HardDriveTypeForm()

    if request.htmx:

        form = HardDriveTypeForm(request.POST)
        if form.is_valid():
            form.save()

        hard_drive_types = HardDriveType.objects.all()

        context = {
            "hard_drive_types" : hard_drive_types,
        }

        return render(request, 'components/hard_drive_types.html', context)
    
    if request.method == 'GET':
        hard_drive_types = HardDriveType.objects.all()
        context = {
            "hard_drive_types" : hard_drive_types,
            "form" : form,
        }
        return render(request, 'maintainer/configuration.html', context)


@login_required(login_url='main:login')
@group_required('Maintainer')
def delete_hard_drive_type(request, pk):
    HardDriveType.objects.get(pk = pk).delete()
    hard_drive_types = HardDriveType.objects.all()
    context = {
        "hard_drive_types" : hard_drive_types,
    }
    return render(request, 'components/hard_drive_types.html', context)
