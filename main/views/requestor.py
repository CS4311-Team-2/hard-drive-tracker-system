from itertools import chain

from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.db.models import F, Func, Value, CharField

from main.views.decorators import group_required
from main.models.hard_drive import HardDrive
from main.models.request import Request


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
def view_request(request):
    return render(request, 'requestor/make_request.html')