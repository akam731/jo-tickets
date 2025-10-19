from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test


def is_employee(user):
    return user.is_authenticated and user.is_employee


@login_required
@user_passes_test(is_employee)
def scan_view(request):
    return render(request, "control/scan.html", {"title": "Scan des Billets"})
