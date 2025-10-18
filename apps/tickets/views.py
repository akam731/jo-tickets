"""Vues de l’application."""

from django.http import HttpResponse


def ping(request):
    return HttpResponse("tickets app ready")


