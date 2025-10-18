"""Routage de l’application."""

from django.urls import path
from . import views


app_name = "orders"

urlpatterns = [
    path("commandes/", views.orders_list_view, name="orders_list"),
]


