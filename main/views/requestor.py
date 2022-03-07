from itertools import chain

from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.db.models import F, Func, Value, CharField

from main.views.decorators import group_required
from main.models.hard_drive import HardDrive
from main.models.request import Request
from main.models.event import Event
from main.models.hard_drive_request import HardDriveRequest

from time import time


@login_required(login_url='main:login')
@group_required('Requestor')
def home(request):
    requests        = Request.objects.filter(user = request.user)
    hard_drives     = HardDrive.objects.none()
    for req in requests:
        hard_drives_req = HardDrive.objects.filter(request = req)
        hard_drives = list(chain(hard_drives, hard_drives_req))

    context = {
        "hard_drives"   : hard_drives,
        "requests"      : requests,
        "username"      : request.user.username
        }
    return render(request, 'requestor/home.html', context)

@login_required(login_url='main:login')
@group_required('Requestor')
def view_request(request):
    return render(request, 'requestor/make_request.html')

@login_required(login_url='main:login')
@group_required('Requestor')
def create_hard_drive_request(request):
    if request.method == 'POST':
        HardDriveRequest.objects.create(
            id              = request.POST.get('id'),
            classification  = request.POST.get('classification'),
            amount_required = request.POST.get('amount_required'),
            connection_port = request.POST.get('connection_port'),
            hard_drive_size = request.POST.get('hard_drive_size'),
            hard_drive_type = request.POST.get('hard_drive_type'),
            comment         = request.POST.get('comment'),
        )


def update_request(request, id):
    

        
        

    

@login_required(login_url='main:login')
@group_required('Requestor')
def make_request(request):
    print(request.POST)

    event = Event()
    request_ = Request()
    hard_drive_request = HardDriveRequest()

    if request.method == 'POST': 
        #event = Event()
        event.event_name = request.POST.get('event_name')
        event.event_description = request.POST.get('event_description')
        event.event_type = request.POST.get('event_type')
        event.event_status = request.POST.get('event_status')
        event.event_start_date = request.POST.get('startDate')
        event.event_end_date = request.POST.get('endDate')
        event.event_location = request.POST.get('location')
        event.length_of_reporting_cycle = request.POST.get('lengthOfCycle')
        event.save()

        #request_ = Request()
        request_.status = Request.Request_Status.CREATED
        request_.request_creation_date = time.time()
        request_.request_last_modifed_date = time.time()
        request_.need_drive_by_date = time.time()
        request_.comment = ""
        request_.request_reference_no = Request.objects.latest('request_reference_no') + 1
        request_.request_reference_no_year = time.now().year()
        request_.save()

        if request.POST.get('quantity') != None and request.POST.get('storagesize') != None and request.POST.get('classification') != None and request.POST.get('connection_port') != None and request.POST.get('hard_drive_type') != None:
            #hard_drive_request = HardDriveRequest()
            if(request.POST.get('classification') == '1'):
                hard_drive_request.classification = 'Classified'
            if(request.POST.get('classification') == '2'):
                hard_drive_request.classification = 'Unclassified'
            hard_drive_request.amount_required = request.POST.get('quantity')
            if(request.POST.get('connection_port') == '1'):
                hard_drive_request.connection_port = 'SATA'
            if(request.POST.get('connection_port') == '2'):
                hard_drive_request.connection_port = 'M.2'
            hard_drive_request.hard_drive_size = request.POST.get('storagesize')
            if(request.POST.get('hard_drive_type') == '1'):
                hard_drive_request.hard_drive_type = 'HDD'
            if(request.POST.get('hard_drive_type') == '2'):
                hard_drive_request.hard_drive_type = 'SSD'
            hard_drive_request.comment = request.POST.get('comments')
            #hard_drive_request.request = request_
            hard_drive_request.save()


    all_hd_request = HardDriveRequest.objects.all()
    print("----->",all_hd_request)
    context = {'hard_drive_requests' : all_hd_request}
    return render(request, 'main/requestor_make_request.html', context)