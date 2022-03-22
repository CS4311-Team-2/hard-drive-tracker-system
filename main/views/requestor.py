import http
from itertools import chain

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.forms.models import modelformset_factory

from main.forms import EventForm, HardDriveForm, HardDriveRequestForm
from main.views.decorators import group_required
from main.models.hard_drive import HardDrive
from main.models.request import Request
from main.models.event import Event
from main.models.hard_drive_request import HardDriveRequest

from time import time
from datetime import datetime

# These functions relate to requestor/*.html views. These functions serve only the 
#   requestor role. 

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
def add_hard_drive_request(http_request):
    if 'Add' in http_request.POST:
        print('Adding Request')
        request = Request.objects.get(pk =  http_request.POST.get('request'))
        request.comment = http_request.POST.get('comments')
        request.save()

        print('Adding Event')
        event = Event.objects.filter(request = request)[0]
        event.event_name                = http_request.POST.get('event_name')
        event.event_description         = http_request.POST.get('event_description')
        event.event_type                = http_request.POST.get('event_type')
        event.event_status              = http_request.POST.get('event_status')
        event.event_start_date          = datetime.strptime(http_request.POST.get("startDate"), "%Y-%m-%d")
        event.event_end_date            = datetime.strptime(http_request.POST.get("endDate"), "%Y-%m-%d")
        event.event_location            = http_request.POST.get('c')
        event.length_of_reporting_cycle = http_request.POST.get('lengthOfCycle')
        event.save()

        print('Adding HardDriveRequest')
        HardDriveRequest.objects.create(
            id              = http_request.POST.get('id'),
            classification  = http_request.POST.get('classification'),
            amount_required = http_request.POST.get('quantity'),
            connection_port = http_request.POST.get('connection_port'),
            hard_drive_size = http_request.POST.get('storagesize'),
            hard_drive_type = http_request.POST.get('hard_drive_type'),
            comment         = http_request.POST.get('comment', ''),
            request         = request,
        )

        return redirect('main:update_request', id=request.request_reference_no)

    if 'Create Request' in http_request.POST:
        return redirect('main:index')


@login_required(login_url='main:login')
@group_required('Requestor')
def view_single_request(http_request, id):
    request             = Request.objects.get(pk = id)
    event               = Event.objects.filter(request = request)[0]
    hard_drive_requests = HardDriveRequest.objects.filter(request = request) 

    context = {
        'request'               : request,
        'event'                 : event,  
        'hard_drive_requests'   : hard_drive_requests              
    }    
    
    return render(http_request, 'requestor/make_request.html', context)


@login_required(login_url='main:login')
@group_required('Requestor')
def make_request(http_request):
    if http_request.htmx:
        HDRFormSet = modelformset_factory(model=HardDriveRequest, form=HardDriveRequestForm)
        
        ids = list()
        for form in HDRFormSet(http_request.POST):
            ids.append(form.save().id)

        print('ids: ', ids)

        formset = HDRFormSet(queryset=HardDriveRequest.objects.filter(id__in=ids))
        event_form = EventForm(http_request.POST)
        

        context = {
            'event_form' : event_form,
            'hdr_forms' : formset,
        }

        return render(http_request, 'components/request_form.html', context)


    if http_request.method == 'GET':
        event_form = EventForm()
        HDRFormSet = modelformset_factory(model=HardDriveRequest, form=HardDriveRequestForm)
        formset = HDRFormSet(queryset=HardDriveRequest.objects.none())

        context = {
            'event_form' : event_form,
            'hdr_forms' : formset,
        }
        return render(http_request, 'requestor/make_request.html', context)


    if http_request.method == 'POST': 
        print('POST')
        event_form = EventForm(http_request.POST)
        HDRFormSet = modelformset_factory(model=HardDriveRequest, form=HardDriveRequestForm)
        

        if event_form.is_valid() and HDRFormSet(http_request.POST).is_valid():
            request = Request()
            request.save()

            event = event_form.instance
            event.request = request
            event.save()

            for form in HDRFormSet(http_request.POST):
                hard_drive_request = form.save()
                hard_drive_request.request = request
                hard_drive_request.save()
            
            return redirect('/admin')
        else:
            print(event_form.errors.as_data())
            print(HDRFormSet(http_request.POST).errors.as_data())


    

