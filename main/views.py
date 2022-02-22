# Create your views here.
from django.shortcuts import redirect, render
from .models import Listings
from .forms import ListingForm
from .models import HardDrive

def index(request):
    return render(request, 'main/index.html')

def maintainer_home(request):
    drives = HardDrive.objects.filter(statue= 'delinquent')
    context = {"drives" : drives}
    return render(request, 'main/maintainer_home.html', context)


    
def all_listings(request):
    all_listings = Listings.objects.order_by('-list_date')
    context = {'all_listings': all_listings}
    return render(request, 'main/all_listings.html', context)

def new_listing(request):
    if request.method != 'POST':
        form = ListingForm()
    else:
        form = ListingForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('main:all_listings')
      
    context = {'form': form}
    return render(request, 'main/new_listing.html', context)