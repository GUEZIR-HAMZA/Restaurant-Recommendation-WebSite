from django import forms
from django.contrib.auth import get_user_model


class LoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)

    def clean_username(self):
        username = self.cleaned_data['username']
        user = get_user_model().objects.filter(username=username).first()
        if user is None:
            raise forms.ValidationError('Invalid username.')
        return username


class RegisterForm(forms.Form):
    username = forms.CharField(max_length=100)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

    def clean_email(self):
        email = self.cleaned_data['email']
        user = get_user_model().objects.filter(email=email).first()
        if user is not None:
            raise forms.ValidationError('This email is already in use.')
        return email
