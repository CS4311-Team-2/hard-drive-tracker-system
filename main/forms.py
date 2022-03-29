
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from main.models.hard_drive import HardDrive
from main.models.hard_drive_type import HardDriveType
from main.models.event import Event
from main.models.hard_drive_request import HardDriveRequest


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields =['username', 'email', 'password1', 'password2']
        

class HardDriveForm(forms.ModelForm):
    class Meta:
        model = HardDrive
        fields = ['serial_number','manufacturer', 'model_number','hard_drive_type', 
                    'connection_port','hard_drive_size','classification',
                    'justification_for_classification_change', 'hard_drive_image', 'image_version_id','boot_test_status',
                    'boot_test_expiration','status', 'justification_for_hard_drive_status_change',
                    'issue_date', 'issue_date', 'expected_hard_drive_return_date', 
                    'justification_for_hard_drive_return_date', 'actual_return_date']

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


