from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile
from .models import prodid


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User  # will interact with user model
        fields = ['username', 'email', 'password1', 'password2']


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email']


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image']


class prodidForm(forms.ModelForm):
    prodid = forms.CharField()

    class Meta:
        model = prodid
        fields = ['prodid']
