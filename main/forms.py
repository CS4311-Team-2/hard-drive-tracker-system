from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from main.models.hard_drive import HardDrive
from main.models.event import Event
from main.models.hard_drive_request import HardDriveRequest

JUSTIFICATION_TEXT_BOX = {'cols':85, 'rows':3}

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields =['username', 'email', 'password1', 'password2']
        
class HardDriveForm(forms.ModelForm):
    # TODO: Need to make create_date non-editable. 
    serial_number = forms.CharField(required=True)
    class Meta:
        model = HardDrive
        fields = ['create_date', 'serial_number', 'manufacturer', 'model_number', 
                    'hard_drive_type', 'connection_port', 'hard_drive_size', 'classification',
                    'justification_for_classification_change', 'hard_drive_image', 'image_version_id',
                    'boot_test_status', 'boot_test_expiration', 'status',
                    'justification_for_hard_drive_status_change', 'issue_date', 
                    'expected_hard_drive_return_date', 'justification_for_hard_drive_return_date',
                    'actual_return_date']
        widgets = {
            'justification_for_classification_change': forms.Textarea(attrs={**JUSTIFICATION_TEXT_BOX, 
                                                                                **{"placeholder": "Empty"}}),
            'justification_for_hard_drive_status_change': forms.Textarea(attrs=JUSTIFICATION_TEXT_BOX),
            'justification_for_hard_drive_return_date': forms.Textarea(attrs=JUSTIFICATION_TEXT_BOX), 
            "create_date": forms.SelectDateWidget(),
            "issue_date" : forms.SelectDateWidget(),
            "boot_test_expiration" : forms.SelectDateWidget(),
            'expected_hard_drive_return_date' : forms.SelectDateWidget(),
            'actual_return_date' : forms.SelectDateWidget()
        }

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields =['event_name', 'event_description', 'event_location', 'event_type',
                'length_of_reporting_cycle', 'event_status', 'event_start_date',
                'event_end_date']
        widgets = {
            'event_start_date': forms.SelectDateWidget(),
            'event_end_date': forms.SelectDateWidget()
        }

class HardDriveRequestForm(forms.ModelForm):
    class Meta:
        model = HardDriveRequest
        fields =['classification', 'amount_required', 'connection_port', 
                'hard_drive_size', 'hard_drive_type', 'comment']

