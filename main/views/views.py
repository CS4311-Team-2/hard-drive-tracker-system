# Create your views here.
from django.shortcuts import redirect, render

from main.views import maintainer, requestor, auditor, administrator
from ..forms import CreateUserForm, LoginUserForm
from django.http import Http404

from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.http import Http404

from users.models import UserProfile

MAINTAINER = "Maintainer"

def add_drive(request):
    return render(request, 'maintainer/add_hard_drive.html')

# These functions relate to the account/*.html and main/index.html. These functions relate 
#   to logining in and creating account.  

@login_required(login_url='main:login')
def index(request):
    if is_maintainer(request) | request.user.is_staff:
        return maintainer.home(request)

    if request.user.groups.filter(name='Requestor').exists() | is_maintainer_requestor(request):
        return requestor.home(request)

    if request.user.groups.filter(name = 'Auditor').exists():
        return auditor.home(request)

    if request.user.groups.filter(name = 'Administrator').exists():
        return administrator.view_all_profiles(request)

    return redirect("main:index")

    


@login_required(login_url='main:login')
def view_request(request):
    if is_maintainer(request) | request.user.is_staff:
        return maintainer.view_request(request)
    
    return redirect('main:index')

@login_required(login_url='main:login')
def view_all_requests(request):
    if request.user.groups.filter(name='Maintainer').exists() | request.user.is_staff:
        return maintainer.view_all_requests(request)
    
    return redirect('main:index')

@login_required(login_url='main:login')
def make_request(request):
    print("Make request in VIEW")
    if request.user.groups.filter(name='Requestor').exists() | request.user.is_staff | is_maintainer_requestor(request): 
        return requestor.make_request(request)

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
    context = {
        "show_menu" : False
        }
    if request.user.is_authenticated:
        print("User authorized!")
        user = UserProfile.objects.get(username=request.user.username)
        if request.method == 'POST':
            print("---------------------------")
            form = LoginUserForm(request.POST, instance=user)
            if form.is_valid():
                form.save()
                return redirect('main:index')
            else:
                messages.info(request, form.errors)

        if user.groups.filter(name=Group(name=MAINTAINER)):
            messages.info(request, 'Welcome Maintainer!')
            context = {
                "show_menu" : True,
                'form': LoginUserForm(instance=user)
            }
        else:
            return redirect('main:index')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        auth = authenticate(request, username=username, password=password)

        if auth is not None:
            print("User credentials is correct")
            user = UserProfile.objects.get(username=username)
            # checks if user.status is not pending
            if user.status == UserProfile.Status.PENDING:
                messages.info(request, 'Adminstrator has not approved this account')
                return render(request, 'accounts/login.html', context)
                
            login(request, auth)
            print(user)
            if user.groups.filter(name=Group(name=MAINTAINER)):
                return redirect('main:login')
            else:
                return redirect('main:index')
        else:
            messages.info(request, 'Username or password is incorrect')

    return render(request, 'accounts/login.html', context)

def logoutUser(request):
    logout(request)
    return redirect('main:login')

@login_required(login_url='main:login')
def add_hard_drive(request):
    if request.user.groups.filter(name='Maintainer').exists() | request.user.is_staff:
        return maintainer.add_hard_drive(request)

    if request.user.groups.filter(name='Requestor').exists():
        raise Http404('Unauthorize access')

@login_required(login_url='main:login')
def view_hard_drive(request, id):
    if request.user.is_staff | is_maintainer(request):
        print("MADE IT HERE AS A MAINTAINER")
        return maintainer.view_hard_drive(request, id)

    if (request.user.groups.filter(name='Requestor').exists() | request.user.is_staff | is_maintainer_requestor(request)):
        print("MADE IT HERE AS A REQUESTOR")
        return requestor.view_hard_drive(request, id)

    return redirect('main:index')

@login_required(login_url='main:login')
def view_all_harddrives(request):
    if request.user.is_staff | is_maintainer(request):
        print("MADE IT HERE AS A MAINTAINER")
        return maintainer.view_all_harddrives(request)

    if (request.user.groups.filter(name='Requestor').exists() | request.user.is_staff | is_maintainer_requestor(request)):
        print("MADE IT HERE AS A REQUESTOR")
        return requestor.view_all_hard_drive(request)

    return redirect('main:index')


def configuration(request):
    if request.user.groups.filter(name='Maintainer').exists() | request.user.is_staff:
        return maintainer.configuration(request)
        
    return redirect('main:index')

def is_maintainer(request):
    print(request.user.username)
    user = UserProfile.objects.get(username=request.user.username)
    print(user.groups.filter(name='Maintainer').exists())
    print(user.mock_group_is == UserProfile.MockGroupIs.MAINTAINER)
    return (user.mock_group_is == UserProfile.MockGroupIs.MAINTAINER) and (user.groups.filter(name='Maintainer').exists())

def is_maintainer_requestor(request):
    user = UserProfile.objects.get(username=request.user.username)
    print(user.groups.filter(name='Maintainer').exists())
    print(user.mock_group_is == UserProfile.MockGroupIs.REQUESTOR)
    return (user.mock_group_is == UserProfile.MockGroupIs.REQUESTOR) and (user.groups.filter(name='Maintainer').exists())
    
@login_required(login_url='main:login')
def view_all_profiles(request):
    if request.user.groups.filter(name='Maintainer').exists() | request.user.is_staff:
        return maintainer.view_all_profiles(request)
            
    return redirect('main:index')

@login_required(login_url='main:login')
def audi_view_all_users(request):
    if request.user.groups.filter(name='Auditor').exists() :
        return auditor.audi_view_all_users(request)
