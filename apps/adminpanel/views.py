"""Vues de l’application."""

from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Sum, Count
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


