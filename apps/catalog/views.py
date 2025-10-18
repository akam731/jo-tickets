"""Vues de l’application."""

from django.shortcuts import render
from .models import Offer


def offers_view(request):
    """Liste des offres actives."""
    offers = Offer.objects.filter(is_active=True).order_by("price")
    return render(request, "catalog/offers.html", {"offers": offers})


