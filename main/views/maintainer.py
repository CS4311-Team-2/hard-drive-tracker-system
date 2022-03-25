from asyncio import events
from multiprocessing import context
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required

from datetime import datetime
from main.models import request
from main.models.hard_drive_request import HardDriveRequest

from main.views.decorators import group_required
from main.models.hard_drive import HardDrive
from main.models.request import Request
from main.models.event import Event

# These functions relate to maintainer/*.html views. These functions serve only the 
#   maintainer role. 



@login_required(login_url='main:login')
@group_required('Maintainer')
def home(request):
    deliquentdrives = HardDrive.objects.filter(status= 'delinquent')
    requests = Request.objects.all()
    context = {
        "deliquentdrives" : deliquentdrives, 
        "requests" : requests,
        }
    return render(request, 'maintainer/home.html', context)

@login_required(login_url='main:login')
@group_required('Maintainer')
def view_request(http_request, key_id):
    print("before")
    req = Request.objects.get(request_reference_no = key_id)
    print("here")

    # used for event information
    events = Event.objects.filter(request = req)
    event = events[0]
    
    #used for assigned hard drive sections
    hard_drives = HardDrive.objects.filter(request = req)
    
    #used for the selecting hard drive section
    all_hard_drives = HardDrive.objects.all()
    
    #used for requested hard drive
    requested_hard_drives = HardDriveRequest.objects.filter(request = req)
    print(requested_hard_drives[0].classification)

    context = {'req' : req, 'event' :event, 'hard_drives' :hard_drives, 'all_hard_drives' : all_hard_drives, 'requested_hard_drives' : requested_hard_drives }
    return render(http_request, 'maintainer/view_request.html', context)

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
        print('here1')
        data[r] = event
        print("here2")
    print(data)

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