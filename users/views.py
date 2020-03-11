from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required

from .models import *
from accounts.models import *
from .forms import *
from .decorators import unauthenticated_user, allowed_users

#@login_required(login_url='login') - insert above views to be restricted

@unauthenticated_user
def registerPage(request):
    
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')

            group = Group.objects.get(name='customer') # assigns new user to customer group
            user.groups.add(group)
            
            Customer.objects.create(
                user=user,
            )

            messages.success(request, 'Account was created for ' +  username )
            return redirect('login')
    context = {'form': form}
    return render(request, 'users/register.html', context)

@unauthenticated_user
def loginPage(request):
    
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.info(request, 'Username OR Password is incorrect')

        context = {}
        return render(request, 'users/login.html', context)

def logOutUser(request):
    logout(request)
    return redirect('login')

@login_required
@allowed_users(allowed_roles=['customer'])
def userPage(request):
    orders = request.user.customer.order_set.all()

    total_orders = orders.count()
    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count()
    context = {'orders': orders, 'total_orders': total_orders, 'delivered' : delivered, 'pending' : pending}
    return render(request, 'users/user.html', context)

