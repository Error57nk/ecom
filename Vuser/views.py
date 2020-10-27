from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from .forms import CreateUserForm

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from django.contrib import messages
from Store.models import Customer
from . decorators import unauthenticated_user

# Create your views here.


@unauthenticated_user
def regPage(request):

    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        # print ('form submited')
        if form.is_valid():
            form.save()
            uname = form.cleaned_data.get('username')

            # print ("formn Saved")
            messages.success(request, 'Acount was created for: ' + str(uname))
            return redirect('login')

    context = {'form': form}
    return render(request, 'Vuser/registration.html', context)


def logoutUser(request):
    logout(request)
    return redirect('home')


@unauthenticated_user
def loginPage(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(username + "<----->" + password)
        user = authenticate(request, username=username, password=password)

        if user is not None:
            print(" Login sucess ")
            login(request, user)
            player, created = Customer.objects.get_or_create(
                user=request.user, name=request.user, email=request.user.email)
            return redirect('home')
        else:
            messages.info(request, "Username or password is incorrect")

    context = {}
    return render(request, 'Vuser/login.html', context)


@login_required(login_url='login')
def homePage(request):
    context = {}
    return render(request, 'Vuser/home.html', context)


def createCoustomer(request):
    player, created = Customer.objects.get_or_create(
        user=request.user, name=request.user, email=request.user.email)
