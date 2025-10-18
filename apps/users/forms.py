"""Formulaires utilisateurs."""

from django import forms


class SignupForm(forms.Form):
    """Formulaire d’inscription."""

    email = forms.EmailField()
    first_name = forms.CharField(max_length=150)
    last_name = forms.CharField(max_length=150)
    password1 = forms.CharField(widget=forms.PasswordInput())
    password2 = forms.CharField(widget=forms.PasswordInput())


class LoginForm(forms.Form):
    """Formulaire de connexion."""

    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput())
