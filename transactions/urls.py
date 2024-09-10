from django.contrib import admin
from django.urls import path

from . import views

from django.http import HttpResponse

urlpatterns = [
    path('transfer/', views.transfer, name="transfer"),
]