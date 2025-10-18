"""Routage de l’application."""

from django.urls import path
from . import views


app_name = "tickets"

urlpatterns = [
    path("mes-billets/", views.my_tickets_view, name="my_tickets"),
    path("billet/<int:ticket_id>/", views.ticket_detail_view, name="ticket_detail"),
    path("billet/<int:ticket_id>/qr.png", views.ticket_qr_image_view, name="ticket_qr_image"),
]


