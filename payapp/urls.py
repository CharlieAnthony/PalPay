from django.contrib import admin
from django.urls import path

from . import views

from django.http import HttpResponse

urlpatterns = [
    path('dashboard/', views.dashboardView, name="dashboard"),
    path('history/', views.historyView, name="history"),
    path('admin_page/', views.adminView, name="admin"),
    path('admin_page/update_roles/', views.AdminUpdateRoles, name="update_roles"),
    path('request/', views.requestHandle, name="request"),
]