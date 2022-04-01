import django_filters
from django_filters import DateFilter

from .models import HardDrive

class HardDriveFilter(django_filters.FilterSet):
    creation_date = DateFilter(field_name="create_date", lookup_expr="gte", label="Creation Date")
    class Meta:
        model = HardDrive
        fields = ['__all__', 'creation_date']