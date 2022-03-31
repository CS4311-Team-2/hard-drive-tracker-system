import django_filters
from django_filters import DateFilter, CharFilter, ModelMultipleChoiceFilter
from django.contrib.auth.models import User

class UserProfilesFilter(django_filters.FilterSet):
    fname = CharFilter(field_name="first_name", lookup_expr="icontains", label="First Name")
    lname = CharFilter(field_name="last_name", lookup_expr="icontains", label="Last Name")
    email_address = CharFilter(field_name="email", lookup_expr="icontains", label="Email")
    user_name = CharFilter(field_name="username", lookup_expr="icontains", label="Username")
    last_modified_date = DateFilter(field_name="date_joined", lookup_expr="gte", label="Last Modified Date")
    class Meta:
        model = User
        fields = ['fname','lname','email_address','user_name','groups', 'last_modified_date']
