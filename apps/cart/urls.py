"""Routage de l’application."""

from django.urls import path
from . import views


app_name = "cart"

urlpatterns = [
    path("panier/", views.cart_view, name="cart"),
    path("panier/ajouter/", views.add_to_cart_api, name="add_to_cart"),
    path("panier/checkout/", views.checkout_view, name="checkout"),
]


