from django.forms import inlineformset_factory
from django.shortcuts import render, redirect
from .filters import OrderFilter
from .forms import OrderForm, RegisterForm
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .decorators import unauthenticated_user, allowed_user


# Create your views here.


@login_required()
@allowed_user('admin')
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


@login_required(login_url='login')
def customer(request, pk):
    customer = Customer.objects.get(id=pk)
    orders = customer.order_set.all()
    latest = customer.order_set.latest('date_created')
    total = orders.count()
    my_filter = OrderFilter(request.GET, queryset=orders)
    orders = my_filter.qs
    print(orders)
    context = {'orders': orders, 'customer': customer, 'latest': latest, 'total': total, 'my_filter': my_filter}
    return render(request, 'accounts/customer.html', context)


@login_required(login_url='login')
def products(request):
    products = Product.objects.all()
    context = {'Product': products}
    return render(request, 'accounts/products.html', context)


@login_required(login_url='login')
def createorder(request, pk):
    OrderFormSet = inlineformset_factory(Customer, Order, fields=('product', 'status'))
    customer = Customer.objects.get(id=pk)
    # form = OrderForm(initial={'customer':customer})
    formset = OrderFormSet(instance=customer, queryset=Order.objects.none())
    if request.method == 'POST':
        formset = OrderFormSet(request.POST, instance=customer)
        if formset.is_valid():
            formset.save()
        return redirect('/')
    context = {'formset': formset, 'customer': customer}
    return render(request, 'accounts/forms.html', context)


@login_required(login_url='login')
def updateorder(request, pk_update):
    order = Order.objects.get(id=pk_update)
    form = OrderForm(instance=order)
    if request.method == 'POST':
        print('printing post:', request.POST)
        form = OrderForm(request.POST)
        if form.is_valid():
            form.save()
    context = {'forms': form}
    return render(request, 'accounts/forms.html', context)


@login_required(login_url='login')
def deleteorder(request, pk_delete):
    delete = Order.objects.get(id=pk_delete)
    if request.method == "POST":
        delete.delete()
        return redirect('/')
    context = {'delete': delete}
    return render(request, 'accounts/delete.html', context)


@login_required(login_url='login')
def delete_customer(request, pk):
    customer = Customer.objects.get(id=pk)
    if request.method == "POST":
        customer.delete()
        return redirect('/')
    context = {'costumer': customer}
    return render(request, 'accounts/delete_customer.html', context)


@unauthenticated_user
def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'Username or password is incorrect.')
    return render(request, 'accounts/login.html')


def logout_user(request):
    logout(request)
    return redirect('login')


@unauthenticated_user
def register(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        form = RegisterForm()
        if request.method == 'POST':
            form = RegisterForm(request.POST)
            if form.is_valid():
                form.save()
                user = form.cleaned_data.get('username')
                messages.success(request, 'Welcome,', user)
                return redirect('login')

    context = {'form': form}
    return render(request, 'accounts/register.html', context)
