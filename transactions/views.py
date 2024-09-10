import decimal
import requests

from django.shortcuts import render, redirect
from django.db import transaction, OperationalError
from django.contrib import messages
from .forms import TransactionForm
from register.models import CustomUser
from payapp.models import Notification
from django.contrib.auth.decorators import login_required


# Create your views here.

@login_required(login_url='login')
def transfer(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            t = form.save(commit=False)
            transaction_type = form.cleaned_data['transaction_type']
            other_email = form.cleaned_data['other_email']
            amount = form.cleaned_data["amount"]
            currency = form.cleaned_data["currency"]
            other_user = CustomUser.objects.filter(email=other_email).first()
            if not other_user:
                messages.info(request, "User does not exist.")
                return render(request, "transactions/transferform.html", {"form": form})
            elif other_user == request.user:
                messages.info(request, "You cannot transfer money to yourself.")
                return render(request, "transactions/transferform.html", {"form": form})
            if transaction_type == 'send':
                t.sender = request.user
                t.receiver = other_user
            else:
                Notification.objects.create(
                    sender=request.user,
                    receiver=other_user,
                    amount=amount,
                    currency=currency,
                    active=True
                )
                return redirect('dashboard')

            t.save()

            src_username = t.sender
            dst_username = t.receiver

            src_user = CustomUser.objects.get(email=src_username)
            src_balance = src_user.balance
            dst_user = CustomUser.objects.get(email=dst_username)
            dst_balance = dst_user.balance

            if src_balance < amount:
                messages.info(request, f"Insufficient balance.")
                return render(request, "transactions/transferform.html", {"src_balance": src_balance, "dst_balance": dst_balance})

            if not performTransfer(request, src_user, dst_user, amount, currency):
                messages.info(request, f"Transfer operation is not possible now.")
                return render(request, "transactions/transferform.html", {"src_balance": src_balance, "dst_balance": dst_balance})

        return render(request, "transactions/transferform.html", {"src_balance": src_balance, "dst_balance": dst_balance})

    form = TransactionForm()
    return render(request, "transactions/transferform.html", {"form": form})


def performTransfer(request, src_user, dst_user, amount, currency):
    try:
        with transaction.atomic():
            src_amount = convert_currency(amount, currency, src_user.currency)
            src_user.balance = src_user.balance - decimal.Decimal(src_amount)

            dst_amount = convert_currency(amount, currency, dst_user.currency)
            dst_user.balance = dst_user.balance + decimal.Decimal(dst_amount)

            CustomUser.save(src_user)
            CustomUser.save(dst_user)
    except OperationalError:
        return False
    return True

def GBP_to_USD(amount):
    return decimal.Decimal(amount * 1.25)


def GBP_to_EUR(amount):
    return decimal.Decimal(amount * 1.15)


def USD_to_GBP(amount):
    return decimal.Decimal(amount * 0.8)


def USD_to_EUR(amount):
    return decimal.Decimal(amount * 0.92)


def EUR_to_GBP(amount):
    return decimal.Decimal(amount * 0.87)


def EUR_to_USD(amount):
    return decimal.Decimal(amount * 1.09)


def convert_currency(amount, currency_from, currency_to):
    if currency_from == currency_to:
        return amount

    url = "http://localhost:8000/conversion/{}/{}/{}".format(currency_from, currency_to, str(amount))
    response = requests.get(url)

    if response.status_code == 200:
        converted = response.json()['amount']
        return decimal.Decimal(converted)
    else:
        raise Exception("Currency conversion failed")