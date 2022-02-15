from django.shortcuts import render
from django.http import HttpResponse


# Create your views here.

def drive_view(request):
    return HttpResponse('<h1>Our First Drive Yay!!<h1>')

def add_drive_view(request):
    return HttpResponse('<h1>Page to Add a New Hard Drive<h1>')
