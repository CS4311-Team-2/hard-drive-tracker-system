import django_filters
from django_filters import DateFilter, CharFilter, ChoiceFilter
from users.models import UserProfile
from django.db.models import Q


class UserProfilesFilter(django_filters.FilterSet):
    first_name = CharFilter(field_name="first_name", lookup_expr="icontains", label="First Name")
    last_name = CharFilter(field_name="last_name", lookup_expr="icontains", label="Last Name")
    email = CharFilter(field_name="email", lookup_expr="icontains", label="Email")
    username = CharFilter(field_name="username", lookup_expr="icontains", label="Username")
    last_modified_date = DateFilter(field_name="date_joined", lookup_expr="gte", label="Last Modified Date")
    keyword = CharFilter(method='search_all_fields',label="Search")

    class Meta:
        model = UserProfile
        fields = ['first_name','last_name','email','username','groups', 'status', 'last_modified_date', 'keyword']

    def search_all_fields(self, queryset, name, value):
        return queryset.filter(
            Q(first_name__icontains=value) | Q(last_name__icontains=value) | Q(email__icontains=value) | Q(username__icontains=value)
        )