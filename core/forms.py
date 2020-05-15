from django import forms
from django.contrib.auth.forms import UserCreationForm
from django_countries.widgets import CountrySelectWidget

from .models import *

PAYMENT_CHOICES = (
    ('S', 'Stripe'),
    ('P', 'PayPal')
)


class CheckoutForm(forms.Form):
    street_address = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': '1234 Main St',
        'required': True,
        'class': 'form-control'
    }), error_messages={'required': 'Street address is required'})
    apartment_address = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'placeholder': 'Apartment or suite',
        'class': 'form-control'
    }))
    country = CountryField(blank_label='Select country').formfield(widget=CountrySelectWidget(attrs={
        'class': 'custom-select d-block w-100',
        'required': True,
    }), error_messages={'required': 'Country is required'})
    zip = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'required': True,
    }), error_messages={'required': 'Zip is required'})
    same_shipping_address = forms.BooleanField(required=False)
    save_info = forms.BooleanField(required=False)
    payment_option = forms.ChoiceField(widget=forms.RadioSelect, choices=PAYMENT_CHOICES,
                                       error_messages={'required': 'Payment option is required'})


USER_TYPE_CHOICES = (
    ('buyer', 'Buyer'),
    ('seller', 'Seller'),
)


class RegistrationForm(UserCreationForm):
    user_type = forms.ChoiceField(choices=USER_TYPE_CHOICES)

    class Meta:
        model = User
        fields = (
            'username', 'email', 'password1', 'password2', 'user_type')

    def signup(self, request, user):
        user.save()
