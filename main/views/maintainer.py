from urllib import request
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required

from main.forms import CreateUserForm, HardDriveConnectionPortsForm, HardDriveTypeForm, HardDriveManufacturersForm, UserForm, HardDriveSizeForm
from main.views.decorators import group_required
from main.models.hard_drive import HardDrive
from main.models.hard_drive_request import HardDriveRequest
from main.models.request import Request
from main.models.event import Event
from main.models.log import Log
from main.models.configurations.hard_drive_connection_ports import HardDriveConnectionPorts
from main.forms import HardDriveForm
from main.models.configurations.hard_drive_type import HardDriveType
from main.models.configurations.hard_drive_size import HardDriveSize
from main.models.configurations.hard_drive_manufacturers import HardDriveManufacturers
from main.filters import HardDriveFilter, RequestFilter, EventFilter, LogFilter
from users.models import UserProfile 
from main.filters import UserProfilesFilter
from main.views.util import is_in_groups

VIEW_HARD_DRIVE = "view_hard_drive"

# These functions relate to maintainer/*.html views. These functions serve only the 
#   maintainer role. 

@login_required(login_url='main:login')
@group_required('Maintainer')
def home(request):
    requests = Request.objects.filter(request_status = Request.Request_Status.CREATED)
    overdue_requests = Request.objects.filter(request_status = Request.Request_Status.OVERDUE)
    deliquent_drives = HardDrive.objects.none()
    for r in overdue_requests:
        deliquent_drives |= HardDrive.objects.filter(request=r)

    context = {
        "deliquent_drives" : deliquent_drives, 
        "requests" : requests,
    }
    return render(request, 'maintainer/home.html', context)

@login_required(login_url='main:login')
def view_request(http_request, key_id):

    req = Request.objects.get(request_reference_no = key_id)

    # used for event information
    events = Event.objects.filter(request = req)
    event = events[0]
    
    #used for assigned hard drive sections
    hard_drives = HardDrive.objects.filter(request = req)
    print(hard_drives)
    
    #used for the selecting hard drive section
    all_hard_drives = HardDrive.objects.filter(request = None)
    
    #used for requested hard drive
    requested_hard_drives = HardDriveRequest.objects.filter(request = req)
    print(requested_hard_drives[0].classification)

    context = {'req' : req, 'event' :event, 'hard_drives' :hard_drives, 'all_hard_drives' : all_hard_drives, 'requested_hard_drives' : requested_hard_drives }
    return render(http_request, 'maintainer/view_request.html', context)

@login_required(login_url='main:login')
def view_all_requests(http_request):
    data = {}
    requests = Request.objects.all()

    request_filter = RequestFilter(http_request.GET, queryset = requests)
    requests = request_filter.qs

    event_filter = EventFilter()

    for r in requests:
        events = Event.objects.filter(request = r)
        event_filter = EventFilter(http_request.GET, queryset = events)
        events = event_filter.qs
        if not events:
            continue
        else:
            event = events[0]
        data[r] = event

    context = {'data': data, 'requests' : requests, 
                'request_filter': request_filter, 'event_filter': event_filter}
    return render(http_request, 'maintainer/view_all_requests.html', context)

@login_required(login_url='main:login')
def view_all_harddrives(request):
    hard_drives = HardDrive.objects.all()
    
    hard_drive_filter = HardDriveFilter(request.GET, queryset = hard_drives)
    hard_drives = hard_drive_filter.qs

    context = {"hard_drives" : hard_drives, "hard_drive_filter" : hard_drive_filter}
    return render(request, 'maintainer/view_all_hard_drives.html', context)

@login_required(login_url='main:login')
@group_required('Maintainer')
@PendingDeprecationWarning
def view_all_profiles(request):
    '''
    DeprecationWarning
    Please use views.view_all_profiles
    '''
    userProfiles = UserProfile.objects.all()

    profileFilter = UserProfilesFilter(request.GET, queryset=userProfiles)
    userProfiles = profileFilter.qs

    context = {"userProfiles" : userProfiles, "profileFilter" : profileFilter}
    return render(request, 'maintainer/view_all_profiles.html', context)

@login_required(login_url='main:login')
def view_user_profile(request, id):
    userProfile = UserProfile.objects.get(pk = id)
    form = UserForm(instance=userProfile)

    if request.method == 'POST' and is_in_groups(request,"Administrator"):
        form = UserForm(request.POST, instance=userProfile)
        if form.is_valid():
            form.save()
            Log.objects.create(action_performed="Modified User: " + userProfile.username, user=request.user)
            return redirect('main:view_all_profiles')
        else:
            context = {"userProfile" : userProfile,"form" : form}
            return render(request, 'maintainer/view_user_profile.html', context)
    context = {
        "userProfile" : userProfile,
        "form" : form,
        "auditor_view":False
        }
    
    if is_in_groups(request,"Auditor"):
        context['form'].make_all_readonly()
        context['auditor_view'] = True
    return render(request, 'maintainer/view_user_profile.html', context)

@login_required(login_url='main:login')
def create_user_profile(request):
    form = CreateUserForm()
    if(request.method == 'POST'):
        form= CreateUserForm(request.POST)
        if form.is_valid():
            userP = form.save()
            userP.groups.set(form.cleaned_data.get('groups'))
            userP.save()
            Log.objects.create(action_performed="Created the user profile: "+userP.username, user=request.user)
            return redirect('main:view_all_profiles')
        else:
            print(form.errors)
    context = {
         "form": form,
         }
    return render(request, 'maintainer/create_user_profile.html', context)


@login_required(login_url='main:login')
@group_required('Maintainer')
def add_hard_drive(http_request):
    form = HardDriveForm()
    if (http_request.method == 'POST'):
        form = HardDriveForm(http_request.POST)
        if form.is_valid():
            hard_drive = form.save(commit=False)
            hard_drive.modifier = http_request.user
            hard_drive.save()
            Log.objects.create(action_performed="Created the hard drive: " + hard_drive.serial_number, user=http_request.user)
            return redirect('main:index')
        else:
            print(form.errors)
    return render(http_request, 'maintainer/view_hard_drive.html', {'form': form, VIEW_HARD_DRIVE:False}) 

@login_required(login_url='main:login')
@group_required('Maintainer')
def view_hard_drive(http_request, id=-1):
    if id==-1:
        print("ERROR ERROR")    
    hard_drive = HardDrive.objects.filter(pk=id).first()
    modifier = hard_drive.modifier.email

    # Saves new hard drive. 
    if http_request.method == 'POST':
        form = HardDriveForm(http_request.POST, instance=hard_drive)
        if form.is_valid():
            hard_drive = form.save(commit=False)
            hard_drive.modifier = http_request.user
            hard_drive.save()
            Log.objects.create(action_performed="Modified the hard drive: " + hard_drive.serial_number, user=http_request.user)
        else:
            print(form.errors)
    else:
        form = HardDriveForm(instance=hard_drive)
        form['modifier'].initial = modifier
    context = {"form" : form, 'id':id, 
                'email':hard_drive.modifier.email, 
                VIEW_HARD_DRIVE:True, "only_view":False}
    return render(http_request, 'maintainer/view_hard_drive.html', context)

@login_required(login_url='main:login')
@group_required('Maintainer')
def configuration(request):    
    hard_drive_types = HardDriveType.objects.all()
    hard_drive_manufacturers = HardDriveManufacturers.objects.all()
    hard_drive_connection_ports = HardDriveConnectionPorts.objects.all()
    hard_drive_size = HardDriveSize.objects.all()
    context = {
        "hard_drive_types" : hard_drive_types,
        "hard_drive_types_form" : HardDriveTypeForm(),
        "hard_drive_manufacturers": hard_drive_manufacturers,
        "hard_drive_manufacturers_form": HardDriveManufacturersForm(),
        "hard_drive_connection_ports": hard_drive_connection_ports,
        "hard_drive_connection_port_form": HardDriveConnectionPortsForm(),
        "hard_drive_sizes":hard_drive_size, 
        "hard_drive_size_form":HardDriveSizeForm() 
        }
    return render(request, 'maintainer/configuration.html', context)

@login_required(login_url='main:login')
def view_log(request):
    if not is_in_groups(request,"Auditor", "Maintainer"):
        return redirect("main:index")
    logs = Log.objects.all()

    log_filter = LogFilter(request.GET, queryset=logs)
    logs = log_filter.qs

    context = {"Logs" : logs, 'log_filter':log_filter}
    return render(request, 'log/view_log.html', context)

