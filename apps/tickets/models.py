"""Modèles de l’application."""

import secrets
from io import BytesIO
from django.db import models
from django.contrib.auth import get_user_model
from apps.orders.models import Order
import qrcode


User = get_user_model()


class Ticket(models.Model):
    """Billet."""

    STATUS_VALID = "valid"
    STATUS_USED = "used"

    STATUS_CHOICES = [
        (STATUS_VALID, "Valide"),
        (STATUS_USED, "Utilisé"),
    ]

    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name="ticket")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="tickets")
    key2 = models.CharField(max_length=64)
    final_key = models.CharField(max_length=128, unique=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=STATUS_VALID)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "tickets_ticket"
        verbose_name = "Billet"
        verbose_name_plural = "Billets"
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"Billet #{self.id} - {self.user} - {self.status}"

    def save(self, *args, **kwargs) -> None:
        if not self.key2:
            self.key2 = secrets.token_urlsafe(32)
        if not self.final_key and getattr(self.user, "key1", None):
            self.final_key = self.user.key1 + self.key2
        super().save(*args, **kwargs)

    def generate_qr_code(self) -> bytes:
        """Génère le PNG du QR code et retourne les octets."""
        if not self.final_key:
            return b""
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(self.final_key)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        buffer = BytesIO()
        img.save(buffer, format="PNG")
        buffer.seek(0)
        return buffer.getvalue()

    def is_valid(self) -> bool:
        return self.status == self.STATUS_VALID

    def mark_as_used(self) -> bool:
        if self.is_valid():
            self.status = self.STATUS_USED
            self.save(update_fields=["status", "updated_at"])
            return True
        return False


