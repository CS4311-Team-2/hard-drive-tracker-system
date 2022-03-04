from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required

from main.views.decorators import group_required
from main.models.hard_drive import HardDrive
from main.models.request import Request


@login_required(login_url='main:login')
@group_required('Requestor')
def home(request):
    deliquentdrives = HardDrive.objects.filter(status= 'delinquent')
    requests = Request.objects.filter(request_status = 'created')
    context = {"deliquentdrives" : deliquentdrives, "requests" : requests}
    return render(request, 'requestor/home.html', context)

@login_required(login_url='main:login')
@group_required('Requestor')
def view_request(request):
    return render(request, 'requestor/make_request.html')