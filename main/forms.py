from django import forms
from .models import Listings
from main.submodels.hard_drive import HardDrive

# Template class
class ListingForm(forms.ModelForm):
    class Meta:
        model = Listings
        fields = ['title', 'condition', 'product_type', 'sale_type', 'price', 'city', 'state', 'zipcode', 'contact_email', 'list_date']

class HardDriveForm(forms.ModelForm):
    class Meta:
        model = HardDrive
        fields = ['serial_number','manufacturer', 'model_number','hard_drive_type', 
                    'connection_port','hard_drive_size','classification',
                    'justification_for_classification_change', 'image_version_id','boot_test_status',
                    'boot_test_expiration','status', 'justification_for_hard_drive_status_change',
                    'issue_date', 'issue_date', 'expected_hard_drive_return_date', 
                    'justification_for_hard_drive_return_date_status_change', 'actual_return_date']