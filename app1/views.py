from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.forms import inlineformset_factory
from .models import *
from .form import OrderForm,CreateUserForm
from django.contrib.auth.models import User

from .filters import OrderFilter
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate,login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from .decorators import unauthenticated_user, allowed_users, admin_only

# Create your views here.
@unauthenticated_user
def registerpage(request):

    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            userername = form.cleaned_data.get('username')

            group = Group.objects.get(name='customer')
            user.groups.add(group)
            customer.objects.create(
                user=user,
            )
            messages.success(request,'Account was created for '+ userername) 
            return redirect('login')

    context={'form':form}
    return render(request,'app1/register.html',context)

@unauthenticated_user
def loginpage(request):
    
    if request.method == 'POST':
        superusers = User.objects.filter(is_superuser=True)
        print(superusers,'hrer')
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(username=username,password=password)

        if user is not None:
            login(request,user)
            return  redirect('home')
        else:
            messages.info(request,'Username or password is incorrect')

    context = {}
    return render(request,'app1/login.html',context)

def logoutUser(request):
    logout(request)
    # logout is imported from django
    return redirect('login')
    # here login value is from name field in url/login

@login_required(login_url='login')
# @allowed_users(allowed_roles=['admin'])
@admin_only
def home(request):
    orders = order.objects.all()
    customerss = customer.objects.all()
    total_orders = orders.count()
    Delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count()

    context = {'customers':customerss,'orders':orders,'total_orders':total_orders,'Delivered':Delivered,'pending':pending}
    return render(request,'app1/dashboard.html', context)

@allowed_users(allowed_roles=['customer'])
@login_required(login_url='login')
def userpage(request):
    orders = request.user.customer.order_set.all()
    total_orders = orders.count()
    Delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count()
    # print(orders)
    context = {'orders':orders,'total_orders':total_orders,'Delivered':Delivered,'pending':pending}
    return render(request,'app1/user.html',context)

@allowed_users(allowed_roles=['admin'])
@login_required(login_url='login')
def products(request):
    products = product.objects.all()
    return render(request,'app1/products.html',{'products':products})

@allowed_users(allowed_roles=['admin'])
@login_required(login_url='login')
def customers(request,pk):
    customers = customer.objects.get(id=pk)
    orders = customers.order_set.all()
    order_count = orders.count()
    myfilter = OrderFilter(request.GET,queryset=orders)
    orders = myfilter.qs
    context = {'customers':customers,'orders':orders,'order_count':order_count,'myfilter':myfilter}
    return render(request,'app1/customer.html',context)

@login_required(login_url='login')
def createOrder(request,pk):
    OrderFormSet = inlineformset_factory(customer,order, fields=('product','status'),extra=10)
    customerss = customer.objects.get(id=pk)
    formset = OrderFormSet(queryset=order.objects.none(),instance=customerss)

    

    if request.method == 'POST':
        # print('hemanth',request.POST)
        # form = OrderForm(request.POST)
        formset = OrderFormSet(request.POST,instance=customerss)
        if formset.is_valid():
            formset.save()
            return redirect('/')
    context = {'formset':formset}

    return render(request,'app1/order_form.html',context)

@login_required(login_url='login')
def updateOrder(request,pk):
    orders = order.objects.get(id=pk)
    form = OrderForm(instance=orders)

    if request.method == 'POST':
        # print('hemanth',request.POST)
        form = OrderForm(request.POST,instance=orders)
        if form.is_valid():
            form.save()
            return redirect('/')
    context = {'form':form}

    return render(request,'app1/order_form.html',context)

@login_required(login_url='login')
def deleteOrder(request,pk):
    orders = order.objects.get(id=pk)
    if request.method == 'POST':
        orders.delete()
        return redirect('/')
    context = {'item':orders}
    return render(request,'app1/delete_order.html',context)

