from .models import Cart


def cart_context(request):
    """
    Ajoute les informations du panier au contexte de tous les templates.
    """
    context = {
        "cart_items_count": 0,
        "cart_total_price": 0,
    }

    if request.user.is_authenticated:
        try:
            cart = Cart.objects.get(user=request.user)
            context["cart_items_count"] = cart.total_items
            context["cart_total_price"] = float(cart.total_price)
        except Cart.DoesNotExist:
            # Le panier sera créé automatiquement lors du premier ajout
            pass

    return context
