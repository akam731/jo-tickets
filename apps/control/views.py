"""Vues de l’application."""

from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test


def is_employee(user):
    return user.is_authenticated and (user.is_staff or user.is_superuser)


@login_required
@user_passes_test(is_employee)
def scan_view(request):
    """Page de scan des billets pour les employés."""
    return render(request, "control/scan.html")


