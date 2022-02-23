# Create your views here.
from django.shortcuts import redirect, render
from .models import Listings
from .forms import ListingForm, CreateUserForm

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

def index(request):
    return render(request, 'main/index.html')

    
def all_listings(request):
    all_listings = Listings.objects.order_by('-list_date')
    context = {'all_listings': all_listings}
    return render(request, 'main/all_listings.html', context)

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
            return redirect('/login/')
    
    context = {'form': form}
    return render(request, 'accounts/register.html', context)
    
def loginPage(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('')

    context = {}
    return render(request, 'accounts/login.html', context)

def home(request):
    pass

def products(request):
    pass
