from django.contrib import admin
from django.urls import path

from . import views

from django.http import HttpResponse

urlpatterns = [
    path('', views.home),
    path('register/', views.registerPage, name="register"),
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutUser, name="logout"),
]