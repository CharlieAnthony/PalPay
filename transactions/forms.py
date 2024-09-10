from django import forms
from payapp import models

class TransactionForm(forms.ModelForm):
    TRANSACTION_TYPE_CHOICES = [
        ('send', 'Send Money'),
        ('request', 'Request Money'),
    ]
    transaction_type = forms.ChoiceField(choices=TRANSACTION_TYPE_CHOICES, widget=forms.RadioSelect)
    other_email = forms.EmailField()
    class Meta:
        model = models.Transaction
        fields = ["amount", "currency"]