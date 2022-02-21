from django import forms
from .models import Listings
from main.submodels.hard_drive import *

# Template class
class ListingForm(forms.ModelForm):
    class Meta:
        model = Listings
        fields = ['title', 'condition', 'product_type', 'sale_type', 'price', 'city', 'state', 'zipcode', 'contact_email', 'list_date']

class HardDriveForm(forms.ModelForm):
    class Meta:
        model = HardDrive
        fields = ['create_date', 'manufacturer', 'hard_drive_type', 'connection_port', 
                'status', 'serial_number', 'classification', 'image_version_id', 
                'boot_test_expiration', 'boot_test_status', 'justification_for_hard_drive_status_change', 
                'connection_port', 'issue_date']