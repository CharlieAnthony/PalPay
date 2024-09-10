from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from .forms import CreateUserForm, LoginForm

from transactions.views import convert_currency


# Create your views here.


def home(request):
    return redirect("login")


def registerPage(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            currency = form.cleaned_data['currency']
            print(currency)
            starting_bal = convert_currency(1000, 'GBP', currency)
            user = form.save(commit=False)
            user.balance = starting_bal
            user.save()
            messages.success(request, 'Account was created for ' + form.cleaned_data.get('first_name'))
            return redirect('login')

    context = {'form': form}
    return render(request, 'register/register.html', context)


def loginPage(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    form = LoginForm()

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.info(request, 'Username OR password is incorrect')

    context = {'form': form}
    return render(request, 'register/login.html', context)

def logoutUser(request):
    logout(request)
    return redirect('login')
