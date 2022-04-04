from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required

from main.forms import HardDriveTypeForm
from main.views.decorators import group_required
from main.models.hard_drive import HardDrive
from main.models.request import Request
from main.models.event import Event

from main.models.log import Log

from main.forms import HardDriveForm
from main.models.configurations.hard_drive_type import HardDriveType


@login_required(login_url='main:login')
@group_required('Maintainer')
def delete_hard_drive_type(request, pk):
    HardDriveType.objects.get(pk = pk).delete()
    hard_drive_types = HardDriveType.objects.all()
    context = {
        "hard_drive_types" : hard_drive_types,
    }
    return render(request, 'components/hard_drive_types.html', context)


@login_required(login_url='main:login')
@group_required('Maintainer')
def hard_drive_type(request):
    print("------------------Hello World!!!")
    form = HardDriveTypeForm(request.POST)
    if form.is_valid():
        form.save()
    hard_drive_types = HardDriveType.objects.all()
    context = {"hard_drive_types" : hard_drive_types,}
    return render(request, 'components/hard_drive_types.html', context)


