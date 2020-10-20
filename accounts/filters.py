import django_filters

from .models import *


class OrderFilter(django_filters.filterset):
    class Meta:
        models = Order
        fields = '__all__'
