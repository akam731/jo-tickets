"""Routage de l’application."""

from django.urls import path
from . import views


app_name = "adminpanel"

urlpatterns = [
    path("administration/", views.dashboard_view, name="dashboard"),
    path("administration/offres/", views.offers_crud_view, name="offers_crud"),
]


