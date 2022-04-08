from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from main.models.hard_drive import HardDrive
from main.models.hard_drive_type import HardDriveType
from main.models.event import Event
from main.models.hard_drive_request import HardDriveRequest
from main.models.request import Request


FORM_CONTROL = {'class':'form-control'}
UNEDTIABLE_DATE = {**FORM_CONTROL, **{'readonly': 'readonly'}}

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields =['username', 'email', 'password1', 'password2']
        
class HardDriveForm(forms.ModelForm):
    class Meta:
        model = HardDrive
        fields = ['create_date', 'serial_number', 'manufacturer', 'model_number', 
                    'hard_drive_type', 'connection_port', 'hard_drive_size', 'classification',
                    'justification_for_classification_change', 'hard_drive_image', 'image_version_id',
                    'boot_test_status', 'boot_test_expiration', 'status',
                    'justification_for_hard_drive_status_change', 'issue_date', 
                    'expected_hard_drive_return_date', 'justification_for_hard_drive_return_date',
                    'actual_return_date', 'request']
        widgets = {
            'justification_for_classification_change': forms.TextInput(attrs=FORM_CONTROL),
            'justification_for_hard_drive_status_change': forms.TextInput(attrs=FORM_CONTROL),
            'justification_for_hard_drive_return_date': forms.TextInput(attrs=FORM_CONTROL),

            'serial_number' : forms.TextInput(attrs=FORM_CONTROL), 
            'manufacturer' : forms.TextInput(attrs=FORM_CONTROL),
            'model_number' : forms.TextInput(attrs=FORM_CONTROL),
            'hard_drive_type' : forms.TextInput(attrs=FORM_CONTROL),
            'connection_port' : forms.TextInput(attrs=FORM_CONTROL),
            'hard_drive_size' : forms.TextInput(attrs=FORM_CONTROL),
            'classification' : forms.TextInput(attrs=FORM_CONTROL),
            'hard_drive_image' : forms.TextInput(attrs=FORM_CONTROL),
            'image_version_id' : forms.TextInput(attrs=FORM_CONTROL),
            'boot_test_status' : forms.TextInput(attrs=FORM_CONTROL),
            'status' : forms.TextInput(attrs=FORM_CONTROL),
            'request' : forms.TextInput(attrs=FORM_CONTROL),
            


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
    def __init__(self, *args, **kwargs):
        super(HardDriveRequestForm, self).__init__(*args, **kwargs)
        self.fields['hard_drive_type'] = forms.ChoiceField(
            choices=[ (o.name, str(o.name)) for o in HardDriveType.objects.all()]
        )

    class Meta:
        model = HardDriveRequest
        fields =['classification', 'amount_required', 'connection_port', 
                'hard_drive_size', 'hard_drive_type', 'comment']

class HardDriveTypeForm(forms.ModelForm):
    class Meta:
        model = HardDriveType
        fields =['name']

        widgets = {
            'name' : forms.TextInput(attrs={'class': 'form-control'}),
        }


