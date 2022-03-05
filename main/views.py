# Create your views here.
from email import message
import re
import time
from django.shortcuts import redirect, render
from .models import Listings
from .forms import ListingForm
from .models.event import *
from .models.request import *
from .models.hard_drive import * 
#from .models import *
from .forms import ListingForm, CreateUserForm
from datetime import datetime

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required

@login_required(login_url='main:login')
def index(request):
    return render(request, 'main/index.html')


#@login_required(login_url='main:login')
def maintainer_home(request):
    drives = HardDrive.objects.filter(status= 'delinquent')
    requests = Request.objects.filter(request_status = 'pending')
    context = {"drives" : drives, "request" : requests}
    return render(request, 'main/maintainer_home.html', context)

#@login_required(login_url='main:login')
def requestor_makes_request(request):
    print(request.POST)

    event = Event()
    request_ = Request()
    hard_drive_request = HardDriveRequest()

    if request.method == 'POST':
        if request.POST.get('event_name') != None and request.POST.get('event_description') != None and request.POST.get('event_type') != None and request.POST.get('event_status') != None and request.POST.get('startDate') != None and request.POST.get('endDate') != None  and request.POST.get('location') != None and request.POST.get('lengthOfCycle') != None and request.POST.get('comments') != None: 
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
            request_.status = Request_Status.CREATED
            request_.request_creation_date = time.time()
            request_.request_last_modifed_date = time.time()
            request_.need_drive_by_date = time.time()
            request_.comment = None
            request_.request_reference_no = Request.objects.latest('request_reference_no') + 1
            request_.request_reference_no_year = datetime.now().year()
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




    
def all_listings(request):
    all_listings = Listings.objects.order_by('-list_date')
    context = {'all_listings': all_listings}
    return render(request, 'main/all_listings.html', context)

@login_required(login_url='main:login')
def new_listing(request):
    if request.method != 'POST':
        form = ListingForm()
    else:
        form = ListingForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('main:all_listings')
      
    context = {'form': form}
    return render(request, 'main/new_listing.html', context)

#====================================================================
#                           Accounts 
#====================================================================

def registerPage(request):
    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            messages.success(request, 'Account was created for ' + user)
            return redirect('/login')
    
    context = {'form': form}
    return render(request, 'accounts/register.html', context)
    
def loginPage(request):
    if request.user.is_authenticated:
        return redirect('main:index')


    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password1')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            messages.info(request, 'Username or password is incorrect')

    context = {}
    return render(request, 'accounts/login.html', context)

def logoutUser(request):
    logout(request)
    return redirect('/login')

def home(request):
    pass

def products(request):
    pass
