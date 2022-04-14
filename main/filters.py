from multiprocessing.sharedctypes import Value
import django_filters
from main.models import request
from users.models import UserProfile
from django.db.models import Q, Count
from .models import HardDrive, Request, Event
from django import forms

class DateInput(forms.DateInput):
    input_type = 'date'

class UserProfilesFilter(django_filters.FilterSet):
    first_name = django_filters.CharFilter(field_name="first_name", lookup_expr="icontains", label="First Name")
    last_name = django_filters.CharFilter(field_name="last_name", lookup_expr="icontains", label="Last Name")
    email = django_filters.CharFilter(field_name="email", lookup_expr="icontains", label="Email")
    username = django_filters.CharFilter(field_name="username", lookup_expr="icontains", label="Username")
    last_modified_date = django_filters.DateFilter(field_name="date_joined", lookup_expr="gte", label="Last Modified Date")
    keyword = django_filters.CharFilter(method='search_all_fields',label="Search")

    class Meta:
        model = UserProfile
        fields = ['first_name','last_name','email','username','groups', 'status', 'last_modified_date', 'keyword']

    def search_all_fields(self, queryset, name, value):
        return queryset.filter(
            Q(first_name__icontains=value) | Q(last_name__icontains=value) | Q(email__icontains=value) | Q(username__icontains=value)
        )

class RequestFilter(django_filters.FilterSet):
    request_keyword = django_filters.CharFilter(method='search_all_request_fields',label="Request Keyword")

    class Meta:
        model = Request
        fields = ['request_reference_no', 'request_status', 'request_keyword']

    def search_all_request_fields(self, queryset, name, value):
        return queryset.filter(
            Q(request_reference_no__icontains=value) | Q(request_status__icontains=value) 
        )

class EventFilter(django_filters.FilterSet):
    event_name = django_filters.CharFilter(field_name="event_name", lookup_expr="icontains", label="Event Name")
    event_start_date = django_filters.DateFilter(field_name="event_start_date", lookup_expr="gte", label="Event Start Date", widget=DateInput(attrs={'type': 'date'}))
    event_end_date = django_filters.DateFilter(field_name="event_end_date", lookup_expr="lte", label="Event End Date", widget=DateInput(attrs={'type': 'date'}))
    event_keyword = django_filters.CharFilter(method='search_all_event_fields',label="Event Keyword")

    class Meta:
        model = Event
        fields = ['event_name', 'event_type', 'event_start_date', 'event_end_date', 'event_keyword']

    def search_all_event_fields(self, queryset, name, value):
        return queryset.filter(
            Q(event_name__icontains=value) | Q(event_type__icontains=value) | Q(event_start_date__icontains=value) | Q(event_end_date__icontains=value)
        )

class HardDriveFilter(django_filters.FilterSet):
    
    class Meta:
        model = HardDrive
        fields = '__all__'

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

