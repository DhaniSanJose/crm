from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.contrib.auth.models import User
from django.conf import settings
from django.contrib.auth import authenticate, login, logout

# Create your views here.
from .models import *
from .forms import OrderForm, CreateUserForm, CustomerForm
from .filters import OrderFilter
from .decorators import unauthenticated_user, allowed_users, admin_only
from os.path import splitext
import os

def registerPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        form = CreateUserForm()

        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid():
                user = form.save()
                username = form.cleaned_data.get('username')
              
                # user.groups.add(group)
                # Customer.objects.create(
                #     user=user,
                #     name=user.username,
                # )
                messages.success(request,'Account was created for ' + username)

                return redirect('login')

        context = {'form':form}
        return render(request, 'accounts/register.html', context)
    


@unauthenticated_user
def loginPage(request):
    if request.method == 'POST':
        username=request.POST.get('username')
        password=request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'username and password is incorrect')

    context = {}
    return render(request, 'accounts/login.html', context)

def logoutUser(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
@admin_only
def home(request):
    orders = Order.objects.all()
    customers = Customer.objects.all()
    
    total_customers = customers.count()
    total_orders = orders.count()
    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count()
    
    context = {'orders':orders, 'customers':customers, 
    'total_orders':total_orders, 'delivered': delivered,
    'pending': pending }
    
    return render(request, 'accounts/dashboard.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def userPage(request):
    orders = request.user.customer.order_set.all()
    total_orders = orders.count()
    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count()
    print('ORDERS:', orders )
    context = {'orders':orders, 
               'total_orders':total_orders, 
               'delivered': delivered,
               'pending': pending}
    return render(request, 'accounts/user.html', context)

# @login_required(login_url='login')
# @allowed_users(allowed_roles=['customer'])
# def accountSettings(request):
#     customer = request.user.customer
#     form = CustomerForm(instance=customer)

#     if request.method == 'POST':
#         form = CustomerForm(request.POST,request.FILES, instance=customer)
#         if form.is_valid():
#             form.save()

#     context = {'form':form}
#     return render(request, 'accounts/account_settings.html', context)


#WORKING UPLOAD TO CHANGE TO CUSTOMER NAME
# @login_required(login_url='login')
# @allowed_users(allowed_roles=['customer'])
# def accountSettings(request):
#     customer = request.user.customer
#     form = CustomerForm(instance=customer)

#     if request.method == 'POST':
#         form = CustomerForm(request.POST, request.FILES, instance=customer)
#         if form.is_valid():
#             # Save form data
#             form.save()

#             # Rename the profile picture if it exists
#             if 'profile_pic' in request.FILES:
#                 # Get the uploaded profile picture
#                 profile_picture = request.FILES['profile_pic']

#                 # Rename the profile picture file using the customer's name
#                 customer_name = customer.name  # Assuming 'name' is the field storing the customer's name
#                 file_name, file_extension = os.path.splitext(profile_picture.name)
#                 new_file_name = f"{customer_name}_profile_picture{file_extension}"

#                 # Construct the correct file path
#                 file_path = os.path.join(settings.MEDIA_ROOT, new_file_name)

#                 # Rename the file in the filesystem
#                 with open(file_path, 'wb+') as destination:
#                     for chunk in profile_picture.chunks():
#                         destination.write(chunk)

#                 # Update the profile picture name in the customer object
#                 customer.profile_pic.name = new_file_name
#                 customer.save()

#     context = {'form': form}
#     return render(request, 'accounts/account_settings.html', context)
# END WORKING UPLOAD TO CHANGE TO CUSTOMER NAME

@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def accountSettings(request):
    customer = request.user.customer
    form = CustomerForm(instance=customer)

    if request.method == 'POST':
        form = CustomerForm(request.POST, request.FILES, instance=customer)
        if form.is_valid():
            # Save form data
            form.save()

            # Rename the profile picture if it exists
            if 'profile_pic' in request.FILES:
                # Get the uploaded profile picture
                profile_picture = request.FILES['profile_pic']

                # Rename the profile picture file using the username
                username = request.user.username
                file_name, file_extension = os.path.splitext(profile_picture.name)
                new_file_name = f"{username}{file_extension}"

                # Construct the correct file path
                file_path = os.path.join(settings.MEDIA_ROOT, new_file_name)

                # Rename the file in the filesystem
                with open(file_path, 'wb+') as destination:
                    for chunk in profile_picture.chunks():
                        destination.write(chunk)

                # Update the profile picture name in the customer object
                customer.profile_pic.name = new_file_name
                customer.save()

    context = {'form': form}
    return render(request, 'accounts/account_settings.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def products(request):
    products = Product.objects.all()
    
    return render(request, 'accounts/products.html', {'products':products})
    

def customer(request, pk_test):
    customer = Customer.objects.get(id=pk_test)
    orders = customer.order_set.all()
    orders_count = orders.count()
    myFilter = OrderFilter(request.GET, queryset=orders)
    orders = myFilter.qs
  
    context = {'customer':customer, 'orders':orders, 'orders_count':orders_count,'myFilter':myFilter}
    return render(request, 'accounts/customer.html', context)

def createOrder(request, pk):
    OrderFormSet = inlineformset_factory(Customer, Order, fields = ('product', 'status'), extra=10)
    customer = Customer.objects.get(id=pk)
    formset = OrderFormSet(queryset=Order.objects.none(), instance=customer)
    #form = OrderForm(initial={'customer': customer})
    if request.method == 'POST':
    # print('Printing POST', request.POST)
        # form = OrderForm(request.POST)
        formset = OrderFormSet(request.POST, instance=customer)
        if formset.is_valid():
            formset.save()
            return redirect('/')
    context = {'formset':formset}
    return render(request, 'accounts/order_form.html', context)
    
    
def updateOrder(request, pk):
    order = Order.objects.get(id=pk)
    formset = OrderForm(instance=order)
    
    if request.method == 'POST':
    
        formset = OrderForm(request.POST, instance=order)
        if formset.is_valid():
            formset.save()
            return redirect('/')
    
    context = {'formset':formset}
    return render(request, 'accounts/order_form.html', context) 

def deleteOrder(request, pk):
    order = Order.objects.get(id=pk)
    if request.method == "POST":
        order.delete()
        return redirect('/')
    
    context = {'item':order}
    return render(request, 'accounts/delete.html', context)