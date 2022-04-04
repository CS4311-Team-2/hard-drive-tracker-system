from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required

from main.forms import HardDriveTypeForm, HardDriveManufacturersForm, HardDriveConnectionPortsForm
from main.views.decorators import group_required
from main.models.configurations.hard_drive_type import HardDriveType
from main.models.configurations.hard_drive_manufacturers import HardDriveManufacturers
from main.models.configurations.hard_drive_connection_ports import HardDriveConnectionPorts

@login_required(login_url='main:login')
@group_required('Maintainer')
def hard_drive_type(request):
    print("----------\nHard Drive Type\n-------")
    form = HardDriveTypeForm(request.POST)
    if form.is_valid():
        form.save()
    hard_drive_types = HardDriveType.objects.all()
    context = {"hard_drive_types" : hard_drive_types,}
    return render(request, 'components/hard_drive_types.html', context)

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
def hard_drive_manufacturer(request):
    print("----------\nHard Drive Manufacturer\n-------")
    form =  HardDriveManufacturersForm(request.POST)
    if form.is_valid():
        form.save()
    hard_drive_manufacturers = HardDriveManufacturers.objects.all()
    context = {"hard_drive_manufacturers" : hard_drive_manufacturers,}
    return render(request, 'components/hard_drive_manufacturers.html', context)

@login_required(login_url='main:login')
@group_required('Maintainer')
def delete_hard_drive_manufacturer(request, pk):
    HardDriveManufacturers.objects.get(pk = pk).delete()
    hard_drive_manufacturers = HardDriveManufacturers.objects.all()
    context = {
        "hard_drive_manufacturers" : hard_drive_manufacturers,
    }
    return render(request, 'components/hard_drive_manufacturers.html', context)

@login_required(login_url='main:login')
@group_required('Maintainer')
def hard_drive_connection_port(request):
    print("----------\nHard Drive Connection Port\n-------")
    form =  HardDriveConnectionPortsForm(request.POST)
    if form.is_valid():
        form.save()
    hard_drive_connection_port = HardDriveConnectionPorts.objects.all()
    context = {"hard_drive_connection_ports" : hard_drive_connection_port,}
    return render(request, 'components/hard_drive_connection_port.html', context)

@login_required(login_url='main:login')
@group_required('Maintainer')
def delete_hard_drive_connection_port(request, pk):
    HardDriveConnectionPorts.objects.get(pk = pk).delete()
    hard_drive_connection_port = HardDriveConnectionPorts.objects.all()
    context = {
        "hard_drive_connection_ports" : hard_drive_connection_port,
    }
    return render(request, 'components/hard_drive_connection_port.html', context)


