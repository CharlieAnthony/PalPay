from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
# from django.contrib.auth.models import User
from .models import CustomUser


User = get_user_model()

class CreateUserForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2', 'currency']


class LoginForm(AuthenticationForm):
    class Meta:
        username = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'autofocus': True}))
        model = CustomUser
        fields = ['email', 'password']
