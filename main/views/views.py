# Create your views here.
from django.shortcuts import redirect, render

from main.views.decorators import group_required
from main.views import maintainer, requestor
from ..models import HardDrive
from ..models import Request
from ..forms import ListingForm, CreateUserForm

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required


def add_drive(request):
    return render(request, 'maintainer/add_hard_drive.html')
    
@login_required(login_url='main:login')
def index(request):
    if request.user.groups.filter(name='Maintainer').exists() | request.user.is_staff:
        return maintainer.home(request)

    if request.user.groups.filter(name='Requestor').exists():
        return requestor.home(request)


@login_required(login_url='main:login')
def view_request(request):
    if request.user.groups.filter(name='Maintainer').exists() | request.user.is_staff:
        return maintainer.view_request(request)
    
    return redirect('main:index')

@login_required(login_url='main:login')
def make_request(request):
    if request.user.groups.filter(name='Requestor').exists() | request.user.is_staff:
        return requestor.view_request(request)

    return redirect('main:index')

def registerPage(request):
    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            messages.success(request, 'Account was created for ' + user)
            return redirect('main:login')
    
    context = {'form': form}
    return render(request, 'accounts/register.html', context)
    
def loginPage(request):
    if request.user.is_authenticated:
        return redirect('main:index')


    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('main:index')
        else:
            messages.info(request, 'Username or password is incorrect')

    context = {}
    return render(request, 'accounts/login.html', context)

def logoutUser(request):
    logout(request)
    return redirect('main:login')
