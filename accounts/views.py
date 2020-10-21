from django.forms import inlineformset_factory
from django.shortcuts import render, redirect
from .filters import OrderFilter
from .forms import OrderForm
from .models import *


# Create your views here.
def home(request):
    products = Product.objects.all()
    customers = Customer.objects.all()
    orders = Order.objects.all()
    num_orders = Order.objects.count()
    delivered = Order.objects.filter(status='Delivered').count()
    pending = Order.objects.filter(status='Pending').count()
    context = {'Product': products, 'orders': orders, 'customers': customers, 'num_orders': num_orders,
               'delivered': delivered, 'pend': pending}
    return render(request, 'accounts/dashboard.html', context)


def customer(request, pk):
    customer = Customer.objects.get(id=pk)
    orders = customer.order_set.all()
    latest = customer.order_set.latest('date_created')
    total = orders.count()
    my_filter = OrderFilter(request.GET, queryset=orders) 
    orders= my_filter.qs
    context = {'orders': orders, 'customer': customer, 'latest': latest, 'total': total, 'my_filter': my_filter}
    return render(request, 'accounts/customer.html', context)


def products(request):
    products = Product.objects.all()
    context = {'Product': products}
    return render(request, 'accounts/products.html', context)


def createorder(request, pk):
    OrderFormSet = inlineformset_factory(Customer, Order, fields=('product', 'status'))
    customer = Customer.objects.get(id=pk)
    # form = OrderForm(initial={'customer':customer})
    formset = OrderFormSet(instance=customer, queryset=Order.objects.none())
    if request.method == 'POST':
        print('printing post:', request.POST)
        formset = OrderFormSet(request.POST, instance=customer)
        return redirect('/')
    context = {'formset': formset, 'customer': customer}
    return render(request, 'accounts/forms.html', context)


def updateorder(request, pk_update):
    order = Order.objects.get(id=pk_update)
    form = OrderForm(instance=order)
    if request.method == 'POST':
        print('printing post:', request.POST)
        form = OrderForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
    context = {'forms': form}
    return render(request, 'accounts/forms.html', context)


def deleteorder(request, pk_delete):
    delete = Order.objects.get(id=pk_delete)
    if request.method == "POST":
        delete.delete()
        return redirect('/')
    context = {'delete': delete}
    return render(request, 'accounts/delete.html', context)


def delete_customer(request, pk):
    customer = Customer.objects.get(id=pk)
    if request.method == "POST":
        customer.delete()
        return redirect('/')
        context={'customer':customer}
        return render(request, 'accounts/delete_customer.html', context)
