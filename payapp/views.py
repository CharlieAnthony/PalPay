from django.db.models import Q
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from register.models import CustomUser
from transactions.forms import TransactionForm
from transactions.views import performTransfer
from .models import Transaction, Notification
from django.contrib import messages




# Create your views here.

@login_required(login_url='login')
def dashboardView(request):
    if request.user.currency == 'GBP':
        indicator = '£'
    elif request.user.currency == 'USD':
        indicator = '$'
    else:
        indicator = '€'

    notifications = Notification.objects.filter(receiver=request.user).order_by('-timestamp')[0:5]
    context = {
        'indicator': indicator,
        'notifications': notifications,
    }
    return render(request, "payapp/home.html", context)


@login_required(login_url='login')
def historyView(request):
    history = Transaction.objects.filter(
        Q(sender=request.user) | Q(receiver=request.user)
    ).order_by('-timestamp')
    context = {
        'history': history,
    }
    return render(request, "payapp/history.html", context)


@login_required(login_url='login')
def adminView(request):
    if not request.user.is_staff:
        return redirect('dashboard')
    users = CustomUser.objects.all()
    transactions = Transaction.objects.all()
    context = {
        'users': users,
        'transactions': transactions,
    }
    return render(request, "payapp/admin.html", context)


@login_required(login_url='login')
def AdminUpdateRoles(request):
    if not request.user.is_staff:
        return redirect('dashboard')
    if request.method == 'POST':
        admin_ids = request.POST.getlist('is_admin')
        CustomUser.objects.all().update(is_staff=False)
        CustomUser.objects.filter(id__in=admin_ids).update(is_staff=True)
        CustomUser.objects.filter(id=request.user.id).update(is_staff=True)
        messages.info(request, f"Roles updated successfully.")
        return redirect('update_roles')
    return redirect('admin')


@login_required(login_url='login')
def requestHandle(request):
    if request.method == 'POST':
        notification_id = request.POST.get('notification_id')
        action = request.POST.get('submit')
        if action == 'Accept':
            notification = Notification.objects.get(id=notification_id)
            if notification.receiver.balance < notification.amount:
                messages.info(request, f"Insufficient balance.")
                return redirect('dashboard')
            if not performTransfer(request, notification.receiver, notification.sender, notification.amount, notification.currency):
                messages.info(request, f"Transfer operation is not possible now.")
                return redirect('dashboard')
            Transaction.objects.create(sender=notification.receiver, receiver=notification.sender, amount=notification.amount, currency=notification.currency)
            notification.active = False
            notification.save()
        elif action == 'Decline':
            notification = Notification.objects.get(id=notification_id)
            notification.active = False
            notification.save()
    return redirect('dashboard')