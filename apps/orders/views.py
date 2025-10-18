"""Vues de l’application."""

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Order


@login_required
def orders_list_view(request):
    """Vue liste des commandes."""
    orders = Order.objects.filter(user=request.user).order_by('-created_at').select_related('offer')
    return render(request, 'orders/orders.html', {"orders": orders})


