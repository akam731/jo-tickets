"""Modèles de l’application."""

from decimal import Decimal
from django.db import models
from django.core.validators import MinValueValidator


class Offer(models.Model):
    """Offre de billets."""

    OFFER_TYPES = [
        ("solo", "Solo (1 personne)"),
        ("duo", "Duo (2 personnes)"),
        ("familiale", "Familiale (4 personnes)"),
    ]

    name = models.CharField(max_length=50, choices=OFFER_TYPES, unique=True)
    capacity = models.PositiveIntegerField()
    price = models.DecimalField(
        max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal("0.01"))]
    )
    is_active = models.BooleanField(default=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "catalog_offer"
        verbose_name = "Offre"
        verbose_name_plural = "Offres"
        ordering = ["price"]

    def __str__(self) -> str:
        return f"{self.get_name_display()} - {self.price}€ ({self.capacity} personne{'s' if self.capacity > 1 else ''})"

    def get_capacity_display(self) -> str:
        if self.capacity == 1:
            return "1 personne"
        return f"{self.capacity} personnes"

    def is_available(self) -> bool:
        return self.is_active


