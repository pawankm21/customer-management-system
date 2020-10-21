import django_filters
from django.forms.widgets import TextInput
from django_filters import *
from .models import *


class OrderFilter(django_filters.FilterSet):
    start_date = DateFilter(field_name='date_created',lookup_expr='gte',widget=TextInput(attrs={'placeholder': 'date'}))
    end_date = DateFilter(field_name='date_created',lookup_expr='lte',widget=TextInput(attrs={'placeholder': 'filter by date'}))
    note = CharFilter(field_name='note',widget=TextInput(attrs={'placeholder': 'search note'}))
    class Meta:
        model = Order
        fields = '__all__'
        exclude =['customer','date_created']
     
