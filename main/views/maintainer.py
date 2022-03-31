from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.core.management import call_command
from django.forms.models import modelformset_factory


from datetime import datetime
from main.forms import HardDriveTypeForm
from main.models import hard_drive_type

from main.views.decorators import group_required
from main.models.hard_drive import HardDrive
from main.models.request import Request
from main.models.event import Event

from main.models.log import Log

from main.forms import HardDriveForm
from main.models.hard_drive_type import HardDriveType
from django import db

from django.contrib.auth.models import User 


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
def add_hard_drive(request):
    hardDrive = HardDrive()
    
    if (request.method == 'POST'):
        print(f'creation_date: {datetime.strptime(request.POST.get("creation_date"), "%Y-%m-%d")}')
        hardDrive.create_date = datetime.strptime(request.POST.get("creation_date"), "%Y-%m-%d")
        hardDrive.serial_number = request.POST.get('serial_No')
        hardDrive.manufacturer = request.POST.get('manufacturer') 
        hardDrive.model_number = request.POST.get('model_NO')
        hardDrive.hard_drive_type = request.POST.get('hard_drive_type')
        hardDrive.connection_port = request.POST.get('connection_port') 
        hardDrive.hard_drive_size = request.POST.get('hard_drive_size') 
         
        print(f'{request.POST.get("classification")}')
        if (request.POST.get('classification') == 1):
            hardDrive.classification = HardDrive.Classification.CLASSIFIED
        else:
            hardDrive.classification = HardDrive.Classification.UNCLASSIFIED
            
        hardDrive.justification_for_classification_change = request.POST.get('justification_for_classification_change')
        hardDrive.image_version_id = request.POST.get('image_version_id')
        hardDrive.boot_test_status = request.POST.get('boot_test_status')
        print(f'boot_test_expiration_date: {request.POST.get("boot_test_expiration_date")}')
        hardDrive.boot_test_expiration = datetime.strptime(request.POST.get("boot_test_expiration_date"), "%Y-%m-%d")
       
        if (request.POST.get('status') == 1):
            hardDrive.status = 'assigned'
        if (request.POST.get('status') == 2):
            hardDrive.status = 'available'
        if (request.POST.get('status') == 3):
            hardDrive.status = 'end of life'
        if (request.POST.get('status') == 4):
            hardDrive.status = 'master clone'
        if (request.POST.get('status') == 5):
            hardDrive.status = 'pending wipe'
        if (request.POST.get('status') == 6):
            hardDrive.status = 'destroyed'
        if (request.POST.get('status') == 7):
            hardDrive.status = 'lost'
        if (request.POST.get('status') == 8):
            hardDrive.status = 'overdue'
        if (request.POST.get('status') == 9):
            hardDrive.status = 'picked up'
        if (request.POST.get('status') == 10):
            hardDrive.status = 'returned'
        if (request.POST.get('status') == 11):
            hardDrive.status = 'pending classification change approval'
            
        hardDrive.justification_for_hard_drive_status_change = request.POST.get('justification_for_hard_drive_status_change')
        print(f'issue_date: {request.POST.get("issue_date")}')
        hardDrive.issue_date = datetime.strptime(request.POST.get("issue_date"), "%Y-%m-%d")
        print(f'expected_hard_drive_return_date: {request.POST.get("expected_hard_drive_return_date")}')
        hardDrive.expected_hard_drive_return_date = datetime.strptime(request.POST.get("expected_hard_drive_return_date"), "%Y-%m-%d")
        hardDrive.justification_for_hard_drive_return_date = request.POST.get("justification_for_hard_drive_return_date")
        hardDrive.save()

        Log.objects.create(
            action_preformed = "New Hard Drive Added Serial Number: " + request.POST.get('serial_No')
        
        )

        return redirect('main:index')
    
    else:
        print('groups:', request.user.groups)
        return render(request, 'maintainer/add_hard_drive.html', {})

@login_required(login_url='main:login')
@group_required('Maintainer')
def view_all_harddrives(request):
    hardDrives = HardDrive.objects.all()

    context = {"hardDrives" : hardDrives}
    return render(request, 'maintainer/view_all_hard_drives.html', context)

@login_required(login_url='main:login')
@group_required('Maintainer')
def view_all_profiles(request):
    userProfiles = User.objects.all()

    context = {"userProfiles" : userProfiles}
    return render(request, 'maintainer/view_all_profiles.html', context)


@login_required(login_url='main:login')
@group_required('Maintainer')
def view_log(request):
    logs = Log.objects.all()
    context = {"Logs" : logs}
    return render(request, 'log/view_log.html', context)


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

