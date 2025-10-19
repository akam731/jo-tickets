from django.views.generic import ListView
from .models import Offer


class OfferListView(ListView):
    model = Offer
    template_name = "catalog/offers.html"
    context_object_name = "offers"

    def get_queryset(self):
        return Offer.objects.filter(is_active=True).order_by("price")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Nos Offres"
        return context
