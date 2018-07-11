from django import forms
from django.contrib.auth.models import User
from django.forms import ModelForm, HiddenInput, PasswordInput


class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta: 
        model = User
        fields = ["username", "password"]
        help_texts = {
        'username': None,
        'password': None,
    }


class LoginForm(forms.Form):
    username = forms.CharField(max_length=50, 
     widget = forms.TextInput)
    password = forms.CharField(max_length=50, widget=forms.PasswordInput)
    
