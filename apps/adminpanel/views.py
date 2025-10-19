"""Vues de l’application."""

import json
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Sum, Count
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from apps.orders.models import Order
from apps.catalog.models import Offer


def is_adminpanel(user):
    return user.is_authenticated and (user.is_staff or user.is_superuser)


@login_required
@user_passes_test(is_adminpanel)
def dashboard_view(request):
    """Tableau de bord: stats simples des ventes."""
    paid_orders = Order.objects.filter(status=Order.STATUS_PAID)
    total_orders = paid_orders.count()
    total_revenue = paid_orders.aggregate(total=Sum("amount"))[("total")] or 0
    active_offers = Offer.objects.filter(is_active=True).count()

    sales_by_offer = (
        paid_orders.values("offer__name")
        .annotate(count=Count("id"), total=Sum("amount"))
        .order_by("offer__name")
    )

    context = {
        "total_orders": total_orders,
        "total_revenue": total_revenue,
        "active_offers": active_offers,
        "sales_by_offer": sales_by_offer,
    }
    return render(request, "adminpanel/dashboard.html", context)


@login_required
@user_passes_test(is_adminpanel)
def offers_crud_view(request):
    """Page de gestion simple des offres (lecture pour cette étape)."""
    offers = Offer.objects.all().order_by("price")
    return render(request, "adminpanel/offers_crud.html", {"offers": offers})


@login_required
@user_passes_test(is_adminpanel)
@require_http_methods(["GET"])
def offers_api(request):
    offers = Offer.objects.all().order_by("price")
    data = [
        {
            "id": o.id,
            "name": o.name,
            "capacity": o.capacity,
            "price": float(o.price),
            "is_active": o.is_active,
            "description": o.description,
            "created_at": o.created_at.isoformat(),
        }
        for o in offers
    ]
    return JsonResponse({"success": True, "offers": data})


@login_required
@user_passes_test(is_adminpanel)
@require_http_methods(["POST"])
def create_offer_api(request):
    try:
        payload = json.loads(request.body.decode("utf-8"))
    except Exception:
        return JsonResponse({"success": False, "error": "JSON invalide"}, status=400)

    offer = Offer.objects.create(
        name=payload.get("name"),
        capacity=payload.get("capacity"),
        price=payload.get("price"),
        description=payload.get("description", ""),
        is_active=payload.get("is_active", True),
    )
    return JsonResponse(
        {
            "success": True,
            "offer": {
                "id": offer.id,
                "name": offer.name,
                "capacity": offer.capacity,
                "price": float(offer.price),
                "is_active": offer.is_active,
                "description": offer.description,
            },
        }
    )


@login_required
@user_passes_test(is_adminpanel)
@require_http_methods(["PUT"])
def update_offer_api(request, offer_id: int):
    offer = get_object_or_404(Offer, id=offer_id)
    try:
        payload = json.loads(request.body.decode("utf-8"))
    except Exception:
        return JsonResponse({"success": False, "error": "JSON invalide"}, status=400)

    offer.name = payload.get("name", offer.name)
    offer.capacity = payload.get("capacity", offer.capacity)
    offer.price = payload.get("price", offer.price)
    offer.description = payload.get("description", offer.description)
    offer.is_active = payload.get("is_active", offer.is_active)
    offer.save()

    return JsonResponse(
        {
            "success": True,
            "offer": {
                "id": offer.id,
                "name": offer.name,
                "capacity": offer.capacity,
                "price": float(offer.price),
                "is_active": offer.is_active,
                "description": offer.description,
            },
        }
    )


@login_required
@user_passes_test(is_adminpanel)
@require_http_methods(["DELETE"])
def delete_offer_api(request, offer_id: int):
    offer = get_object_or_404(Offer, id=offer_id)
    name = offer.name
    offer.delete()
    return JsonResponse({"success": True, "message": f"Offre '{name}' supprimée"})


