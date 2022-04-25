# Create your views here.
from django.shortcuts import redirect, render

from main.views import maintainer, requestor, auditor, administrator
from ..forms import CreateUserForm, LoginUserForm
from main.views import maintainer, requestor
from ..forms import CreateUserForm, CreateUserFormUser, LoginUserForm, UserForm
from django.http import Http404

from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.http import Http404

from users.models import UserProfile
from main.filters import UserProfilesFilter

from main.views.util import is_in_groups

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
def view_request(request, key_id):
    if is_maintainer(request) | request.user.is_staff:
        return maintainer.view_request(request,key_id)

    if is_in_groups(request, "Requestor"):
        return requestor.edit_request(request,key_id)
    
    return redirect('main:index')

@login_required(login_url='main:login')
def view_all_requests(request):
    if is_maintainer(request) | request.user.is_staff:
        return maintainer.view_all_requests(request)
    
    if is_in_groups(request, "Auditor"):
        return maintainer.view_all_requests(request)


    if is_in_groups(request, "Requestor") | is_maintainer_requestor(request):
        return requestor.view_all_requests(request)
    
    return redirect('main:index')

@login_required(login_url='main:login')
def make_request(request):
    print("Make request in VIEW")
    if request.user.groups.filter(name='Requestor').exists() | request.user.is_staff | is_maintainer_requestor(request): 
        return requestor.make_request(request)

    return redirect('main:index')


@login_required(login_url='main:login')
def edit_request(request, key_id):
    if request.user.groups.filter(name='Requestor').exists() | request.user.is_staff:
        return requestor.edit_request(request, key_id)

    return redirect('main:index')


def registerPage(request):
    form = CreateUserFormUser()
    if request.method == 'POST':
        form = CreateUserFormUser(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            messages.success(request, 'Account was created for ' + user)
            return redirect('main:login')
    
    context = {'form': form}
    return render(request, 'accounts/register.html', context)
    
def loginPage(request):
    context = {
        "show_menu" : False,
        'form': LoginUserForm()
        }

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        auth = authenticate(request, username=username, password=password)

        if auth is not None:
            print("Here")
            user = UserProfile.objects.get(username=username)
            # checks if user.status is not pending
            if user.status == UserProfile.Status.PENDING:
                messages.info(request, 'Adminstrator has not approved this account')
                return render(request, 'accounts/login.html', context)
            form = LoginUserForm(request.POST)
            login(request, auth)
            # Should always work! 
            if is_in_groups(request, form['groups'].value()):
                return redirect('main:index')
            logout(request)
            messages.info(request, 'Username or password is incorrect')
            return render(request, 'accounts/login.html', context)            
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
    #TODO: Clean up this code to utilze is_in_groups
    if request.user.is_staff | is_maintainer(request):
        print("MADE IT HERE AS A MAINTAINER")
        return maintainer.view_hard_drive(request, id)

    if (request.user.groups.filter(name='Requestor').exists() | request.user.is_staff | is_maintainer_requestor(request)):
        print("MADE IT HERE AS A REQUESTOR")
        return requestor.view_hard_drive(request, id)
    
    if is_in_groups(request,"Auditor"):
        # using requestor as auditor cannot edit only view
        return requestor.view_hard_drive(request,id)

    return redirect('main:index')

@login_required(login_url='main:login')
def view_all_harddrives(request):
    print("Before If Statements")
    if request.user.is_staff | is_maintainer(request):
        print("MADE IT HERE AS A MAINTAINER")
        return maintainer.view_all_harddrives(request)
    
    if is_in_groups(request,"Auditor"):
        return maintainer.view_all_harddrives(request)

    if (request.user.groups.filter(name='Requestor').exists() | request.user.is_staff | is_maintainer_requestor(request)):
        print("MADE IT HERE AS A REQUESTOR")
        return requestor.view_all_hard_drive(request)
    print("After If Statements")
    return redirect('main:index')

def configuration(request):
    if is_in_groups(request,'Maintainer'):
        return maintainer.configuration(request)
        
    return redirect('main:index')
    
@login_required(login_url='main:login')
def view_all_profiles(request):
    print('view_all_profiles')
    '''Used by Auditor and Administrator'''
    if not is_in_groups(request, "Auditor", "Administrator"):
        return redirect('main:index')
    
    user_profiles = UserProfile.objects.all()
    profile_filter = UserProfilesFilter(request.GET, queryset=user_profiles)
    user_profiles = profile_filter.qs

    context = {"userProfiles" : user_profiles, "profileFilter" : profile_filter}
    return render(request, 'maintainer/view_all_profiles.html', context)

@login_required(login_url='main:login')
def create_user_profile(request):
    if is_in_groups(request, "Administrator"):
        return maintainer.create_user_profile(request)

    return redirect('main:index')

@login_required(login_url='main:login')
def audi_view_all_users(request):
    if request.user.groups.filter(name='Auditor').exists() :
        return auditor.audi_view_all_users(request)
    print("Error Error at audi_view_all_users")

@login_required(login_url='main:login')
def view_profile(request):
    user = UserProfile.objects.get(username=request.user.username)
    form = CreateUserForm(instance=user)
    form.make_all_readonly()

    return render(request, "maintainer/view_profile.html", {"form":form})

# Util functions, only used to mock a maintainer. 
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

