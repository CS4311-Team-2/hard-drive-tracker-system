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

def maintainer_adds_hard_drive():
    hardDrive = HardDrive()
    
    if add_hard_drive.method == 'POST':
        hardDrive.create_date = add_hard_drive.POST.get('creation_date')
        hardDrive.serial_number = add_hard_drive.POST.get('serial_No')
        hardDrive.manufacturer = add_hard_drive.POST.get('manufacturer')
        hardDrive.model_number = add_hard_drive.POST.get('model_NO')
        hardDrive.hard_drive_type = add_hard_drive.POST.get('hard_drive_type')
        hardDrive.connection_port = add_hard_drive.POST.get('connection_por')
        hardDrive.hard_drive_size = add_hard_drive.POST.get('hard_drive_size')
         
        hardDrive.Classification = add_hard_drive.POST.get('')
        if (hardDrive.POST.get('classification') == 1):
            hardDrive.classification = 'classfied'
        if (hardDrive.POST.get('classification') == 2):
            hardDrive.classification = 'unclassfied'
        hardDrive.justification_for_classification_change = add_hard_drive.POST.get('justification_for_classification_change')
        hardDrive.image = add_hard_drive.POST.get('hardDrive_image')
        hardDrive.image_version_id = add_hard_drive.POST.get('image_version_id')
        hardDrive.boot_test_status = add_hard_drive.POST.get('boot_test_status')
        hardDrive.boot_test_expiration = add_hard_drive.POST.get('boot_test_expiration_date')
       
        #hardDrive.status = add_hard_drive.POST.get('status') How do you get the value for a dropdown?
        hardDrive.justification_for_hard_drive_status_change = add_hard_drive.POST.get('justification_for_hard_drive_status_change')
        hardDrive.issue_date = add_hard_drive.POST.get('issue_date')
        hardDrive.expected_hard_drive_return_date = add_hard_drive.POST.get('expected_hard_drive_return_date')
        hardDrove.justification_for_hard_drive_return_date = add_hard_drive.POST.get('justification_for_hard_drive_return_date')
        hardDrive.request = add_hard_drive.POST.get('request_reference')
        hardDrive.save()
     
        
        
