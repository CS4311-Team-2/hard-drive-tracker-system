import django_filters

from .models import *

class OrderFilter(django_filters.FilterSet):
    class Meta:
        model = HardDrive
        fields = '__all__'