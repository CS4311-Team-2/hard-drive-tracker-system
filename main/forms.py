from django import forms
from .models import Listings
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User

class ListingForm(forms.ModelForm):
    class Meta:
        model = Listings
        fields = ['title', 'condition', 'product_type', 'sale_type', 'price', 'city', 'state', 'zipcode', 'contact_email', 'list_date']

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields =['username', 'email', 'password1', 'password2']