from django import forms
from django.contrib.auth.forms import UserCreationForm
from matplotlib import widgets
from main.models.hard_drive import HardDrive
from main.models.configurations.hard_drive_type import HardDriveType
from main.models.configurations.hard_drive_manufacturers import HardDriveManufacturers
from main.models.configurations.hard_drive_connection_ports import HardDriveConnectionPorts
from main.models.configurations.hard_drive_size import HardDriveSize
from main.models.event import Event
from main.models.hard_drive_request import HardDriveRequest
from main.models.request import Request
from main.models.amendment import Admendment
from users.models import UserProfile


FORM_CONTROL = {'class':'form-control'}
FORM_CONTROL_DATE = {'class':'form-control', 'type':'Date'}
UNEDTIABLE = {**FORM_CONTROL, **{'readonly': 'readonly'}}
UNEDTIABLE_DATE = {**FORM_CONTROL, **{'readonly': 'readonly'}}

# TODO: If possible we need to combine these forms
# Used for only Maintainers creating an account
class CreateUserForm(UserCreationForm):
    class Meta:
        model = UserProfile
        fields =['first_name','last_name','username','groups', 'status', 'email','direct_supervisor_email', 'branch_chief_email', 'password1', 'password2']

    def make_all_readonly(self):
        for field_name in self.fields:
            self.fields[field_name].widget.attrs = UNEDTIABLE

# Used for a user creating an account on the register page
class CreateUserFormUser(UserCreationForm):
    class Meta:
        model = UserProfile
        fields =['first_name','last_name','username','email', 'password1', 'password2']


class UserForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields =['first_name','last_name','email','username','groups', 'status', 'last_modified_date','direct_supervisor_email', 'branch_chief_email']
        
    def make_all_readonly(self):
        for field_name in self.fields:
            self.fields[field_name].widget.attrs = UNEDTIABLE

class HardDriveForm(forms.ModelForm):
        # This does not refer to the acutal modifier field, used to dipslay the field in the template. 
    modifier = forms.CharField(widget=forms.TextInput(attrs=UNEDTIABLE))
    def __init__(self, *args, **kwargs):
        super(HardDriveForm, self).__init__(*args, **kwargs)
        self.fields['hard_drive_type'] = forms.ChoiceField( 
            choices=[ (o.name, str(o.name)) for o in HardDriveType.objects.all()])
        self.fields['hard_drive_type'].widget.attrs = FORM_CONTROL
        self.fields['manufacturer'] = forms.ChoiceField( 
            choices=[ (o.name, str(o.name)) for o in HardDriveManufacturers.objects.all()])
        self.fields['manufacturer'].widget.attrs = FORM_CONTROL
        self.fields['connection_port'] = forms.ChoiceField( 
            choices=[ (o.name, str(o.name)) for o in HardDriveConnectionPorts.objects.all()])
        self.fields['connection_port'].widget.attrs = FORM_CONTROL
        self.fields['hard_drive_size'] = forms.ChoiceField( 
            choices=[ (o.name, str(o.name)) for o in HardDriveSize.objects.all()])
        self.fields['hard_drive_size'].widget.attrs = FORM_CONTROL
        self.fields['modifier'].required = False
    class Meta:
        model = HardDrive
        fields = ['create_date', 'serial_number','manufacturer', 'model_number', 'modified_date',  
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
            'model_number' : forms.TextInput(attrs=FORM_CONTROL),
            'hard_drive_size' : forms.TextInput(attrs=FORM_CONTROL),
            'classification' : forms.Select(attrs=FORM_CONTROL),
            'hard_drive_image' : forms.TextInput(attrs=FORM_CONTROL),
            'image_version_id' : forms.TextInput(attrs=FORM_CONTROL),
            'boot_test_status' : forms.Select(attrs=FORM_CONTROL),
            'status' : forms.Select(attrs=FORM_CONTROL),
            'modified_date' : forms.DateInput(attrs=UNEDTIABLE),
            "create_date":forms.DateInput(attrs=UNEDTIABLE),
            "issue_date" : forms.TextInput(attrs=FORM_CONTROL_DATE),
            "boot_test_expiration" : forms.TextInput(attrs=FORM_CONTROL_DATE),
            'expected_hard_drive_return_date' : forms.TextInput(attrs=FORM_CONTROL_DATE),
            'actual_return_date' : forms.TextInput(attrs=FORM_CONTROL_DATE)
        }
    def clean_image_version_id(self):
        image_version_id = self.cleaned_data.get("image_version_id")
        try: 
            if int(image_version_id) > 10000:
                raise forms.ValidationError("This value is to big")
        except ValueError:
            raise forms.ValidationError("Needs to be a number")
        return image_version_id

    def clean_status(self):
        status = self.cleaned_data.get('status')
        classification = self.cleaned_data.get('classification')
        if status == HardDrive.Status.PENDING_WIPE and classification == HardDrive.Classification.UNCLASSIFIED:
            raise forms.ValidationError("This status can only be assigned to classified drives")
        return status

    def make_all_readonly(self):
        # TODO: This functions is duplicated, find way to only do it once. 
        for field_name in self.fields:
            self.fields[field_name].widget.attrs = UNEDTIABLE

class HardDriveRequestForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(HardDriveRequestForm, self).__init__(*args, **kwargs)
        self.fields['hard_drive_type'] = forms.ChoiceField(
            choices=[ (o.name, str(o.name)) for o in HardDriveType.objects.all()]
        )
        self.fields['hard_drive_type'].widget.attrs = FORM_CONTROL
        
        self.fields['connection_port'] = forms.ChoiceField( 
            choices=[ (o.name, str(o.name)) for o in HardDriveConnectionPorts.objects.all()])
        self.fields['connection_port'].widget.attrs = FORM_CONTROL
        
        self.fields['hard_drive_size'] = forms.ChoiceField( 
            choices=[ (o.name, str(o.name)) for o in HardDriveSize.objects.all()])
        self.fields['hard_drive_size'].widget.attrs = FORM_CONTROL

        self.fields['amount_required'].widget.attrs = FORM_CONTROL
        self.fields['classification'].widget.attrs = FORM_CONTROL
        

    class Meta:
        model = HardDriveRequest
        fields =['classification', 'amount_required', 'connection_port', 
                'hard_drive_size', 'hard_drive_type', 'comment']
    def make_all_readonly(self):
        # TODO: This functions is duplicated, find way to only do it once. 
        for field_name in self.fields:
            self.fields[field_name].widget.attrs = UNEDTIABLE

class HardDriveTypeForm(forms.ModelForm):
    class Meta:
        model = HardDriveType
        fields =['name']

        widgets = {
            'name' : forms.TextInput(attrs={'class': 'form-control'}),
        }
    def make_all_readonly(self):
        # TODO: This functions is duplicated, find way to only do it once. 
        for field_name in self.fields:
            self.fields[field_name].widget.attrs = UNEDTIABLE

class HardDriveManufacturersForm(forms.ModelForm):
    class Meta:
        model = HardDriveManufacturers
        fields =['name']

        widgets = {
            'name' : forms.TextInput(attrs={'class': 'form-control'}),
        }

class HardDriveConnectionPortsForm(forms.ModelForm):
    class Meta:
        model = HardDriveConnectionPorts
        fields =['name']

        widgets = {
            'name' : forms.TextInput(attrs={'class': 'form-control'}),
        }

class HardDriveSizeForm(forms.ModelForm):
    class Meta:
        model = HardDriveSize
        fields =['name']

        widgets = {
            'name' : forms.TextInput(attrs={'class': 'form-control'}),
        }

class LoginUserForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields =['mock_group_is']
        widgets = {
            'mock_group_is': forms.Select(attrs=FORM_CONTROL)
        }

class RequestForm(forms.ModelForm):
    request_creation_date = forms.CharField(widget=forms.TextInput(attrs=FORM_CONTROL))
    request_last_modified_date = forms.CharField(widget=forms.TextInput(attrs=FORM_CONTROL))
    modifier = forms.CharField(widget=forms.TextInput(attrs=UNEDTIABLE))
    requestor = forms.CharField(widget=forms.TextInput(attrs=UNEDTIABLE))
    request_reference_no = forms.CharField(widget=forms.TextInput(attrs=UNEDTIABLE))

    # These are only used for viewing a request via the Requestor
    total_amount_of_drives_requested = forms.CharField(widget=forms.TextInput(attrs=UNEDTIABLE))
    total_amount_of_drives_assigned = forms.CharField(widget=forms.TextInput(attrs=UNEDTIABLE))

    def __init__(self,*args, **kwargs):
        super(RequestForm, self).__init__(*args, **kwargs)
        for field_name in self.fields:
            self.fields[field_name].widget.attrs = FORM_CONTROL
    class Meta:
        model = Request
        fields = ['request_reference_no_year','request_status','need_drive_by_date','comment']
        widgets = {}

    def make_all_readonly(self):
        # TODO: This functions is duplicated, find way to only do it once. 
        for field_name in self.fields:
            self.fields[field_name].widget.attrs = UNEDTIABLE


class EventForm(forms.ModelForm):

    def __init__(self,*args, **kwargs):
        super(EventForm, self).__init__(*args, **kwargs)
        for field_name in self.fields:
            self.fields[field_name].widget.attrs = FORM_CONTROL
    class Meta:
        model = Event
        fields =['event_name', 'event_description', 'event_location', 'event_type',
                'length_of_reporting_cycle', 'event_status', 'event_start_date',
                'event_end_date','analystNames','teamLeadName']
        widgets = {
            'event_start_date': forms.DateInput(),
            'event_end_date': forms.DateInput(),
            'event_description':forms.TextInput(attrs=FORM_CONTROL),
            'length_of_reporting_cycle':forms.TextInput(attrs=FORM_CONTROL)
        }
    def make_all_readonly(self):
        # TODO: This functions is duplicated, find way to only do it once. 
        for field_name in self.fields:
            self.fields[field_name].widget.attrs = UNEDTIABLE


class AdmendmentForm(forms.ModelForm):

    def __init__(self,*args, **kwargs):
        super(AdmendmentForm, self).__init__(*args, **kwargs)
        for field_name in self.fields:
            self.fields[field_name].widget.attrs = FORM_CONTROL
    class Meta:
        model = Admendment
        fields = ['description', 'decision_date', 'comment']
        widgets = {'decision_date':forms.TextInput(attrs=FORM_CONTROL_DATE)}
    def make_all_readonly(self):
        # TODO: This functions is duplicated, find way to only do it once. 
        for field_name in self.fields:
            self.fields[field_name].widget.attrs = UNEDTIABLE

