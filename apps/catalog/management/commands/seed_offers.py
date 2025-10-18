"""Commande de peuplement des offres."""

from django.core.management.base import BaseCommand
from apps.catalog.models import Offer


DEFAULT_OFFERS = [
    {"name": "solo", "capacity": 1, "price": 50.00, "description": "Billet individuel", "is_active": True},
    {"name": "duo", "capacity": 2, "price": 90.00, "description": "Billet pour 2 personnes", "is_active": True},
    {"name": "familiale", "capacity": 4, "price": 160.00, "description": "Billet familial pour 4 personnes", "is_active": True},
]


class Command(BaseCommand):
    help = "Crée ou met à jour les offres par défaut"

    def handle(self, *args, **options):
        created, updated = 0, 0
        for data in DEFAULT_OFFERS:
            obj, is_created = Offer.objects.update_or_create(
                name=data["name"], defaults=data
            )
            if is_created:
                created += 1
            else:
                updated += 1
        self.stdout.write(self.style.SUCCESS(f"Offres: {created} créées, {updated} mises à jour"))
