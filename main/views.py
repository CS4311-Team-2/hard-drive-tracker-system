# Create your views here.
from email import message
from multiprocessing import context
import re
from django.shortcuts import redirect, render
from .models import Listings
from .forms import ListingForm
from .models import HardDrive
from .models import Request
from .forms import ListingForm, CreateUserForm

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required

@login_required(login_url='main:login')
def index(request):
    return render(request, 'main/index.html')


#@login_required(login_url='main:login')
def maintainer_home(request):
    deliquentdrives = HardDrive.objects.filter(status= 'delinquent')
    requests = Request.objects.filter(request_status = 'created')
    context = {"deliquentdrives" : deliquentdrives, "requests" : requests}
    return render(request, 'main/maintainer_home.html', context)

def maintainer_view_request(request):
    return render(request, 'main/maintainer_view_request.html')

def maintainer_view_all_requests(request):
    requests = Request.objects.filter(request_status = 'created')
    context = {"requests" : requests}
    return render(request, 'main/maintainer_view_all_requests.html', context)


    
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
