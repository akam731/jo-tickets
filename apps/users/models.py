"""Modèles de l’application."""

import secrets
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver


User = get_user_model()


@receiver(post_save, sender=User)
def generate_user_key1(sender, instance, created, **kwargs):
    """Génère automatiquement une clé `key1` pour l’utilisateur. """
    if not created:
        return
    if hasattr(instance, "key1") and not getattr(instance, "key1"):
        instance.key1 = secrets.token_urlsafe(32)
        try:
            instance.save(update_fields=["key1"])
        except Exception:
            instance.save()


