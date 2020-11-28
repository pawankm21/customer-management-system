import django_filters
from django.forms.widgets import TextInput
from django_filters import *
from .models import *


class OrderFilter(django_filters.FilterSet):
    start_date = DateFilter(field_name='date_created',lookup_expr='gte',widget=TextInput(attrs={'placeholder':'Ordered after'}))
    end_date = DateFilter(field_name='date_created',lookup_expr='lte',widget=TextInput(attrs={'placeholder':'Ordered before'}))
    status =ChoiceFilter(field_name='status',choices=Order.STATUS,label='none')
    name =django_filters.CharFilter(field_name='name',lookup_expr='icontains',widget=TextInput(attrs={'placeholder':'Product name'}))
    class Meta:
        model = Order
        fields = ('name','start_date',
        'end_date',
        'status',
        
        )
       


class ProductFilter(django_filters.FilterSet):
    price= django_filters.NumberFilter(field_name='price',lookup_expr='lte',widget=TextInput(attrs={'placeholder':'price less than'}))
    name =django_filters.CharFilter(field_name='name',lookup_expr='icontains',widget=TextInput(attrs={'placeholder':'Product name'}))
    category = django_filters.ChoiceFilter(field_name='category',label='Category',choices=Product.CATEGORY,)
    class Meta:
        model = Product
        fields = (
            'name','category','price','tag',
        )
        

class CustomerFilter(django_filters.FilterSet):
    name=django_filters.CharFilter(field_name='name',lookup_expr='icontains',widget=TextInput(attrs={'placeholder':'Customer name'}))
    class Meta:
        models: Customer
        fields =(
            'name'
        )