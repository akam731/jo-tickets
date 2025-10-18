"""Vues de l’application."""

import json
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.middleware.csrf import get_token
from .models import Cart, CartItem
from apps.catalog.models import Offer
from apps.orders.models import Order


@login_required
def cart_view(request):
    cart, _ = Cart.objects.get_or_create(user=request.user)
    items = cart.items.select_related('offer')
    total = sum(item.offer.price * item.quantity for item in items)
    # Assure le jeton CSRF présent dans la page
    get_token(request)
    return render(request, 'cart/cart.html', {"cart": cart, "items": items, "total": total})


@login_required
@require_POST
def add_to_cart_api(request):
    try:
        data = json.loads(request.body.decode('utf-8'))
    except Exception:
        return JsonResponse({"success": False, "message": "JSON invalide"}, status=400)

    offer_id = data.get('offer_id')
    quantity = int(data.get('quantity') or 1)
    if not offer_id:
        return JsonResponse({"success": False, "message": "offer_id requis"}, status=400)

    try:
        offer = Offer.objects.get(id=offer_id, is_active=True)
    except Offer.DoesNotExist:
        return JsonResponse({"success": False, "message": "Offre introuvable"}, status=404)

    cart, _ = Cart.objects.get_or_create(user=request.user)
    item, created = CartItem.objects.get_or_create(cart=cart, offer=offer, defaults={"quantity": quantity})
    if not created:
        item.quantity += quantity
        item.save(update_fields=["quantity"])

    cart_total = sum(ci.quantity for ci in cart.items.all())
    return JsonResponse({"success": True, "message": "Ajouté au panier", "cart_total": cart_total})


@login_required
def checkout_view(request):
    cart, _ = Cart.objects.get_or_create(user=request.user)
    items = list(cart.items.select_related('offer'))
    if request.method == 'POST':
        if not items:
            return redirect('cart:cart')
        total_amount = sum(item.offer.price * item.quantity for item in items)
        # Paiement simulé: création d'une commande payée par article
        for item in items:
            order = Order.objects.create(
                user=request.user,
                offer=item.offer,
                status=Order.STATUS_PAID,
                amount=item.offer.price * item.quantity,
            )
        # Vider le panier
        cart.items.all().delete()
        return render(request, 'cart/confirmation.html', {"total": total_amount})

    total = sum(item.offer.price * item.quantity for item in items)
    return render(request, 'cart/checkout.html', {"items": items, "total": total})


