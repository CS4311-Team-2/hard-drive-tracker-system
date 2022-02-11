from django.shortcuts import render
from django.http import HttpResponse


# Create your views here.

def drive_view(request):
    return HttpResponse('Our First Drive Yay!!')
