"""Routage de l’application."""

from django.urls import path
from . import views


app_name = "catalog"

urlpatterns = [
    path("offres/", views.offers_view, name="offers"),
]


