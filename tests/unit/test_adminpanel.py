from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
import json

from apps.catalog.models import Offer


User = get_user_model()


class AdminPanelApiTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.staff = User.objects.create_user(
            email="staff@example.com",
            username="staff",
            first_name="Staff",
            last_name="User",
            password="MotDePasse123!",
            is_adminpanel=True,
        )
        self.client.force_login(self.staff)

        self.list_url = reverse("adminpanel:offers_api")
        self.create_url = reverse("adminpanel:create_offer_api")

    def test_list_offers_requires_permission(self):
        # Déconnexion puis essayer sans droit
        self.client.logout()
        user = User.objects.create_user(
            email="basic@example.com",
            username="basic",
            first_name="Basic",
            last_name="User",
            password="MotDePasse123!",
        )
        self.client.force_login(user)

        res = self.client.get(self.list_url)
        # user_passes_test renvoie 302 vers login par défaut
        self.assertIn(res.status_code, [302, 403])

    def test_create_update_delete_offer(self):
        # Create
        payload = {
            "name": "familiale",
            "capacity": 4,
            "price": "40.00",
            "description": "Offre familiale",
            "is_active": True,
        }
        res_create = self.client.post(
            self.create_url, data=json.dumps(payload), content_type="application/json"
        )
        self.assertEqual(res_create.status_code, 200)
        offer_id = res_create.json()["offer"]["id"]

        # Update
        update_url = reverse("adminpanel:update_offer_api", args=[offer_id])
        res_update = self.client.put(
            update_url,
            data=json.dumps({"price": "45.00", "is_active": False}),
            content_type="application/json",
        )
        self.assertEqual(res_update.status_code, 200)
        self.assertEqual(res_update.json()["offer"]["price"], 45.0)
        self.assertFalse(res_update.json()["offer"]["is_active"])

        # Delete
        delete_url = reverse("adminpanel:delete_offer_api", args=[offer_id])
        res_delete = self.client.delete(delete_url)
        self.assertEqual(res_delete.status_code, 200)
        self.assertFalse(Offer.objects.filter(id=offer_id).exists())


class AdminPanelAccessTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.dashboard_url = reverse("adminpanel:dashboard")
        self.crud_url = reverse("adminpanel:offers_crud")

    def test_dashboard_and_crud_access(self):
        # Non connecté -> redirect
        res1 = self.client.get(self.dashboard_url)
        res2 = self.client.get(self.crud_url)
        self.assertIn(res1.status_code, [302, 403])
        self.assertIn(res2.status_code, [302, 403])

        # Connecté sans droit -> redirect/403
        user = User.objects.create_user(
            email="u@example.com",
            username="u",
            first_name="U",
            last_name="S",
            password="MotDePasse123!",
        )
        self.client.force_login(user)
        res3 = self.client.get(self.dashboard_url)
        res4 = self.client.get(self.crud_url)
        self.assertIn(res3.status_code, [302, 403])
        self.assertIn(res4.status_code, [302, 403])


