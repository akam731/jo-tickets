"""Commande de peuplement d’utilisateurs de démonstration."""

import os
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model


User = get_user_model()

# Données de démo
USERS = [
    {  # Admin
        "email": "admin@jotickets.com",
        "first_name": "Admin",
        "last_name": "System",
        "username": "admin.system",
        "is_employee": True,
        "is_adminpanel": True,
    },
    {  # Employé
        "email": "employe@jotickets.com",
        "first_name": "Marie",
        "last_name": "Dupont",
        "username": "dupont.marie",
        "is_employee": True,
        "is_adminpanel": False,
    },
    {  # Client 1
        "email": "client@jotickets.com",
        "first_name": "Jean",
        "last_name": "Martin",
        "username": "martin.jean",
        "is_employee": False,
        "is_adminpanel": False,
    },
    {  # Client 2
        "email": "client2@jotickets.com",
        "first_name": "Jean",
        "last_name": "Martin",
        "username": "martin.jean1",
        "is_employee": False,
        "is_adminpanel": False,
    },
    {  # Client 3
        "email": "client3@jotickets.com",
        "first_name": "John",
        "last_name": "Doe",
        "username": "doe.john",
        "is_employee": False,
        "is_adminpanel": False,
    },
]


class Command(BaseCommand):
    help = "Crée/Met à jour des utilisateurs de démonstration (admin, employé, clients)"

    def handle(self, *args, **options):
        # Mots de passe issus du .env
        admin_pwd = os.environ.get("ADMIN_SEED_PASSWORD", "******")
        employee_pwd = os.environ.get("EMPLOYEE_SEED_PASSWORD", "******")
        user_pwd = os.environ.get("USER_SEED_PASSWORD", "******")

        created, updated = 0, 0
        for data in USERS:
            email = data["email"]
            defaults = {
                "first_name": data["first_name"],
                "last_name": data["last_name"],
                "username": data["username"],
                "is_employee": data["is_employee"],
                "is_adminpanel": data["is_adminpanel"],
                "is_staff": bool(data["is_adminpanel"]),
                "is_superuser": bool(data["is_adminpanel"]),
                "is_active": True,
            }

            user, is_created = User.objects.get_or_create(email=email, defaults=defaults)
            if not is_created:
                for k, v in defaults.items():
                    setattr(user, k, v)
                updated += 1
            else:
                created += 1

            # Choix du mot de passe en fonction du rôle
            if defaults["is_adminpanel"]:
                password = admin_pwd
            elif defaults["is_employee"]:
                password = employee_pwd
            else:
                password = user_pwd

            user.set_password(password)
            user.save()

        self.stdout.write(self.style.SUCCESS(f"Utilisateurs: {created} créés, {updated} mis à jour"))
