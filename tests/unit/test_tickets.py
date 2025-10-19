from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
import json

from apps.catalog.models import Offer
from apps.orders.models import Order
from apps.tickets.models import Ticket


User = get_user_model()


class TicketFlowTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            email="ticket@example.com",
            username="ticketuser",
            first_name="Ticket",
            last_name="User",
            password="MotDePasse123!",
        )
        self.client.force_login(self.user)

        self.offer = Offer.objects.create(
            name="duo",
            capacity=2,
            price="20.00",
            description="Offre duo",
            is_active=True,
        )

        self.order = Order.objects.create(
            user=self.user,
            offer=self.offer,
            amount=self.offer.price,
            status="paid",
        )

    def test_ticket_generation_and_qr(self):
        ticket = Ticket.objects.create(order=self.order, user=self.user)
        png = ticket.generate_qr_code()
        self.assertIsInstance(png, (bytes, bytearray))
        self.assertGreater(len(png), 0)

        # Vue image QR
        url = reverse("tickets:ticket_qr_image", args=[ticket.id])
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res["Content-Type"], "image/png")

    def test_validate_ticket_api_success_then_double_use(self):
        ticket = Ticket.objects.create(order=self.order, user=self.user)

        url = reverse("tickets:validate_ticket_api")

        # 1ère validation OK
        res1 = self.client.post(
            url,
            data=json.dumps({"final_key": ticket.final_key}),
            content_type="application/json",
        )
        self.assertEqual(res1.status_code, 200)
        self.assertTrue(res1.json().get("success"))

        # 2ème validation refusée (déjà utilisé)
        res2 = self.client.post(
            url,
            data=json.dumps({"final_key": ticket.final_key}),
            content_type="application/json",
        )
        self.assertEqual(res2.status_code, 400)
        self.assertFalse(res2.json().get("success"))

    def test_get_ticket_info_on_invalid(self):
        url = reverse("tickets:validate_ticket_api")
        res = self.client.post(
            url,
            data=json.dumps({"final_key": "inconnu"}),
            content_type="application/json",
        )
        self.assertEqual(res.status_code, 400)
        self.assertFalse(res.json().get("success"))


