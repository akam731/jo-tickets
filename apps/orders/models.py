"""Modèles de l’application."""

from decimal import Decimal
from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from apps.catalog.models import Offer


User = get_user_model()


class Order(models.Model):
    """Commande de billets."""

    STATUS_PENDING = "pending"
    STATUS_PAID = "paid"
    STATUS_CANCELLED = "cancelled"

    STATUS_CHOICES = [
        (STATUS_PENDING, "En attente de paiement"),
        (STATUS_PAID, "Payé"),
        (STATUS_CANCELLED, "Annulé"),
    ]

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="orders"
    )
    offer = models.ForeignKey(
        Offer, on_delete=models.CASCADE, related_name="orders"
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_PENDING)
    amount = models.DecimalField(
        max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal("0.01"))]
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "orders_order"
        verbose_name = "Commande"
        verbose_name_plural = "Commandes"
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"Commande #{self.id} - {self.user} - {self.offer} - {self.status}"

    def can_be_paid(self) -> bool:
        return self.status == self.STATUS_PENDING

    def can_be_cancelled(self) -> bool:
        return self.status == self.STATUS_PENDING

    def mark_as_paid(self) -> bool:
        if self.can_be_paid():
            self.status = self.STATUS_PAID
            self.save(update_fields=["status", "updated_at"])
            return True
        return False

    def mark_as_cancelled(self) -> bool:
        if self.can_be_cancelled():
            self.status = self.STATUS_CANCELLED
            self.save(update_fields=["status", "updated_at"])
            return True
        return False


