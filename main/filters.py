import django_filters
from django_filters import DateFilter

from .models import HardDrive

class HardDriveFilter(django_filters.FilterSet):
    
    class Meta:
        model = HardDrive
        fields = '__all__'