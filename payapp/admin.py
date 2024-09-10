from django.contrib import admin
from .models import Transaction, Notification

# Register your models here.
admin.site.register(Transaction)
admin.site.register(Notification)