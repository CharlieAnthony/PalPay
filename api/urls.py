from django.urls import path
from . import views

urlpatterns = [
    path('<str:currency1>/<str:currency2>/<str:amount>/', views.convert_currency, name='convert_currency'),
]

