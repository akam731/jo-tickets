"""Modèles de l’application."""

from django.db import models
from django.contrib.auth import get_user_model
from apps.catalog.models import Offer


User = get_user_model()


class Cart(models.Model):
    """Panier d’achat."""

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="cart")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "cart_cart"
        verbose_name = "Panier"
        verbose_name_plural = "Paniers"

    def __str__(self) -> str:
        return f"Panier de {self.user}"


class CartItem(models.Model):
    """Élément de panier."""

    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items")
    offer = models.ForeignKey(Offer, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        db_table = "cart_cartitem"
        verbose_name = "Élément de panier"
        verbose_name_plural = "Éléments de panier"
        unique_together = ("cart", "offer")

    def __str__(self) -> str:
        return f"{self.offer} x{self.quantity}"


