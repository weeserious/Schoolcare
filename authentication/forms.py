from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import *
from django.core.exceptions import ValidationError

class StudentCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not email.endswith('@students.jkuat.ac.ke'):
            raise ValidationError("Invalid email address. Only @students.jkuat.ac.ke domain is allowed.")
        return email


class LoginForm(forms.Form):
    username = forms.CharField(label='username')
    password = forms.CharField(label='password', widget=forms.PasswordInput)
    

class MessageForm(forms.ModelForm):
    content = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control rounded-pill',
        'placeholder': 'Type your message here...',
        'style': 'border: none; box-shadow: none;'
    }))

    class Meta:
        model = Message
        fields = ['content']
