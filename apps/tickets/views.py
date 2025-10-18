"""Vues de l’application."""

from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .models import Ticket


@login_required
def my_tickets_view(request):
    """Liste des billets de l’utilisateur."""
    tickets = Ticket.objects.filter(user=request.user).order_by("-created_at")
    return render(request, "tickets/my_tickets.html", {"tickets": tickets})


@login_required
def ticket_detail_view(request, ticket_id: int):
    """Détail d’un billet utilisateur."""
    ticket = get_object_or_404(Ticket, id=ticket_id, user=request.user)
    return render(request, "tickets/ticket_detail.html", {"ticket": ticket})


@login_required
def ticket_qr_image_view(request, ticket_id: int):
    """Génère et renvoie l’image PNG du QR code."""
    ticket = get_object_or_404(Ticket, id=ticket_id, user=request.user)
    png_bytes = ticket.generate_qr_code()
    response = HttpResponse(png_bytes, content_type="image/png")
    response["Cache-Control"] = "max-age=3600, public"
    return response


