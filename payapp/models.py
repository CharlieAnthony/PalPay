from django.db import models
from django.conf import settings
# Create your models here.


class Transaction(models.Model):
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='sent_transactions', on_delete=models.CASCADE)
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='received_transactions', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, choices=[('GBP', 'Pounds'), ('USD', 'US Dollars'), ('EUR', 'Euros')], default='GBP')
    timestamp = models.DateTimeField(auto_now_add=True)


class Notification(models.Model):
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='sent_notifications', on_delete=models.CASCADE)
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='received_notifications', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, choices=[('GBP', 'Pounds'), ('USD', 'US Dollars'), ('EUR', 'Euros')], default='GBP')
    timestamp = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=False)