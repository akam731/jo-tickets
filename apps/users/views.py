"""Vues de l’application."""

from django.shortcuts import render
from django.contrib.auth.decorators import login_required


def home_view(request):
    """Vue d’accueil."""
    return render(request, "home.html")


def signup_view(request):
    """Vue d’inscription"""
    return render(request, "users/signup.html")


def login_view(request):
    """Vue de connexion"""
    return render(request, "users/login.html")


@login_required
def profile_view(request):
    """Vue de profil utilisateur."""
    return render(request, "users/profile.html")


