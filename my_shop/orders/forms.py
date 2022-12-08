from django import forms
from .models import Order


class OrderCreateForm(forms.ModelForm):
    phone_number = forms.CharField(label='Телефон', max_length=15,
                                   widget=forms.TextInput(attrs={'placeholder': '375XXXXXXXXX'}))

    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'phone_number', 'email', 'address', 'postal_code', 'city']
