from multiprocessing.sharedctypes import Value
import django_filters
from main.models import request
from users.models import UserProfile
from django.db.models import Q, Count
from .models import HardDrive, Request, Event, Log
from django import forms
from django_filters.widgets import RangeWidget

class DateInput(forms.DateInput):
    input_type = 'date'

class UserProfilesFilter(django_filters.FilterSet):
    first_name = django_filters.CharFilter(field_name="first_name", lookup_expr="icontains", label="First Name")
    last_name = django_filters.CharFilter(field_name="last_name", lookup_expr="icontains", label="Last Name")
    email = django_filters.CharFilter(field_name="email", lookup_expr="icontains", label="Email")
    username = django_filters.CharFilter(field_name="username", lookup_expr="icontains", label="Username")
    last_modified_date = django_filters.DateFromToRangeFilter(field_name="date_joined", label="Last Modified Date Range", widget=RangeWidget(attrs={'type': 'date'}))
    keyword = django_filters.CharFilter(method='search_all_fields',label="User Keyword")

    class Meta:
        model = UserProfile
        fields = ['first_name','last_name','email','username','groups', 'status', 'last_modified_date', 'keyword']

    def search_all_fields(self, queryset, name, value):
        return queryset.filter(
            Q(first_name__icontains=value) | Q(last_name__icontains=value) | Q(email__icontains=value) | Q(username__icontains=value) 
            | Q(last_modified_date__icontains=value) | Q(direct_supervisor_email__icontains=value) | Q(branch_chief_email__icontains=value) | Q(status__icontains=value)
        )

class RequestFilter(django_filters.FilterSet):
    request_keyword = django_filters.CharFilter(method='search_all_request_fields',label="Request Keyword")
    request_creation_date = django_filters.DateFromToRangeFilter(field_name="request_creation_date", label="Creation Date Range", widget=RangeWidget(attrs={'type': 'date'}))
    need_drive_by_date = django_filters.DateFromToRangeFilter(field_name="need_drive_by_date", label="Need Drive By Date Range", widget=RangeWidget(attrs={'type': 'date'}))

    class Meta:
        model = Request
        fields = ['request_reference_no', 'request_status', 'request_keyword', 'request_creation_date', 'need_drive_by_date']

    def search_all_request_fields(self, queryset, name, value):
        return queryset.filter(
            Q(request_reference_no__icontains=value) | Q(request_status__icontains=value)  | Q(request_reference_no_year__icontains=value) | Q(request_creation_date__icontains=value) |
            Q(request_last_modified_date__icontains=value) | Q(need_drive_by_date__icontains=value) | Q(comment__icontains=value) |
            Q(event__event_name__icontains=value) | Q(event__event_type__icontains=value) | Q(event__event_start_date__icontains=value) | Q(event__event_end_date__icontains=value) | 
            Q(event__event_description__icontains=value) | Q(event__event_location__icontains=value) | Q(event__length_of_reporting_cycle__icontains=value) | Q(event__event_status__icontains=value) |
            Q(event__analystNames__icontains=value)| Q(event__teamLeadName__icontains=value)
        )

class EventFilter(django_filters.FilterSet):
    event_name = django_filters.CharFilter(field_name="event_name", lookup_expr="icontains", label="Event Name")
    event_start_date = django_filters.DateFromToRangeFilter(field_name="event_start_date", label="Event Start Date Range", widget=RangeWidget(attrs={'type': 'date'}))
    event_end_date = django_filters.DateFromToRangeFilter(field_name="event_end_date", label="Event End Date Range", widget=RangeWidget(attrs={'type': 'date'}))

    class Meta:
        model = Event
        fields = ['event_name', 'event_type', 'event_start_date', 'event_end_date']

class HardDriveFilter(django_filters.FilterSet):
    create_date = django_filters.DateFromToRangeFilter(field_name="create_date", label="Creation Date Range", widget=RangeWidget(attrs={'type': 'date'}))
    issue_date = django_filters.DateFromToRangeFilter(field_name="issue_date", label="Issue Date Range", widget=RangeWidget(attrs={'type': 'date'}))
    modified_date = django_filters.DateFromToRangeFilter(field_name="modified_date", label="Last Modified Date Range", widget=RangeWidget(attrs={'type': 'date'}))
    expected_hard_drive_return_date = django_filters.DateFromToRangeFilter(field_name="expected_hard_drive_return_date", label="Expected Return Date Range", widget=RangeWidget(attrs={'type': 'date'}))
    boot_test_expiration = django_filters.DateFromToRangeFilter(field_name="boot_test_expiration", label="Boot Test Expiration Date Range", widget=RangeWidget(attrs={'type': 'date'}))
    
    serial_number = django_filters.CharFilter(field_name="serial_number", lookup_expr="icontains", label="Serial Number")
    image_version_id = django_filters.CharFilter(field_name="image_version_id", lookup_expr="icontains", label="Image Version ID")
    manufacturer = django_filters.CharFilter(field_name="manufacturer", lookup_expr="icontains", label="Manufacturer")
    model_number = django_filters.CharFilter(field_name="model_number", lookup_expr="icontains", label="Model Number")
    connection_port = django_filters.CharFilter(field_name="connection_port", lookup_expr="icontains", label="Connection Port")
    hard_drive_size = django_filters.CharFilter(field_name="hard_drive_size", lookup_expr="icontains", label="Hard Drive Size")
    hard_drive_type = django_filters.CharFilter(field_name="hard_drive_type", lookup_expr="icontains", label="Hard Drive Type")

    hard_drive_keyword = django_filters.CharFilter(method='search_all_hard_drive_fields',label="Hard Drive Keyword")

    class Meta:
        model = HardDrive
        fields = '__all__'

    def search_all_hard_drive_fields(self, queryset, name, value):
        return queryset.filter(
            Q(create_date__icontains=value) | Q(issue_date__icontains=value)  | Q(modified_date__icontains=value) | Q(expected_hard_drive_return_date__icontains=value) | Q(boot_test_expiration__icontains=value) 
            | Q(serial_number__icontains=value) | Q(image_version_id__icontains=value) |Q(manufacturer__icontains=value) | Q(model_number__icontains=value) | Q(connection_port__icontains=value) 
            | Q(hard_drive_size__icontains=value) | Q(hard_drive_type__icontains=value) |Q(classification__icontains=value) | Q(justification_for_classification_change__icontains=value) | Q(hard_drive_image__icontains=value) 
            | Q(boot_test_status__icontains=value) |Q(status__icontains=value) | Q(justification_for_hard_drive_status_change__icontains=value) | Q(justification_for_hard_drive_return_date__icontains=value)| Q(actual_return_date__icontains=value) 
        )   

class UserProfile(django_filters.FilterSet):
    first_name = django_filters.CharFilter(field_name="first_name", lookup_expr="icontains", label="First Name")
    last_name = django_filters.CharFilter(field_name="last_name", lookup_expr="icontains", label="Last Name")
    email = django_filters.CharFilter(field_name="email", lookup_expr="icontains", label="Email")
    username = django_filters.CharFilter(field_name="username", lookup_expr="icontains", label="Username")

    class Meta:
        model = UserProfile
        fields = ['first_name','last_name','email','username','groups', 'status']   
    def search_all_fields(self, queryset, name, value):
        return queryset.filter(
            Q(first_name__icontains=value) | Q(last_name__icontains=value) | Q(email__icontains=value) | Q(username__icontains=value)
        )

class LogFilter(django_filters.FilterSet):
    time_stamp = django_filters.DateFilter(field_name="time_stamp", lookup_expr="gte", label="Time Stamp From", widget=DateInput(attrs={'type': 'date'}))
    action_performed = django_filters.CharFilter(field_name="action_performed", lookup_expr="icontains", label="Action Performed")
    keyword = django_filters.CharFilter(method='search_all_log_fields',label="Log Keyword")

    class Meta:
        model = Log
        fields = '__all__'

    def search_all_log_fields(self, queryset, name, value):
        return queryset.filter(
            Q(time_stamp__icontains=value)  | Q(action_performed__icontains=value)
        )

