import django_filters
from users.models import UserProfile
from django.db.models import Q
from .models import HardDrive



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

