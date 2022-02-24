# Create your views here.
from email import message
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
    drives = HardDrive.objects.filter(status= 'delinquent')
    requests = Request.objects.filter(request_status = 'pending')
    context = {"drives" : drives, "request" : requests}
    return render(request, 'main/maintainer_home.html', context)


    
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

<<<<<<< HEAD

def detail(request, detail_id):
    detail = Listings.objects.get(id=detail_id)
    context = {'detail': detail}
    return render(request, 'main/detail.html', context)

def edit_listing(request, edit_id):
    listing = Listings.objects.get(id=edit_id)
  
    if request.method != 'POST':
        form = ListingForm(instance=listing)
    else:
        form = ListingForm(request.POST, request.FILES, instance=listing)
        if form.is_valid():
            form.save()
            return redirect('main:all_listings')

    context = {'listing': listing, 'form': form}
<<<<<<< HEAD
    return render(request, 'main/edit_listing.html', context)
=======
    return render(request, 'main/edit_listing.html', context)
>>>>>>> ec1e4124f3ef65649691a3d8d3d91e1a8997c6f5
=======
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
>>>>>>> main
