from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
import json

from apps.catalog.models import Offer
from apps.orders.models import Order


User = get_user_model()


class OrdersTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            email="order@example.com",
            username="orderuser",
            first_name="Order",
            last_name="User",
            password="MotDePasse123!",
        )
        self.client.force_login(self.user)

        self.offer = Offer.objects.create(
            name="solo",
            capacity=1,
            price="10.00",
            description="Offre solo",
            is_active=True,
        )

    def test_create_order_api_and_confirmation(self):
        create_url = reverse("orders:create_order_api")
        res = self.client.post(
            create_url,
            data=json.dumps({"offer_id": self.offer.id}),
            content_type="application/json",
        )
        self.assertEqual(res.status_code, 200)
        order_id = res.json().get("order_id")
        self.assertTrue(Order.objects.filter(id=order_id).exists())

        # Confirmation view (simuler payé)
        order = Order.objects.get(id=order_id)
        order.mark_as_paid()
        confirm_url = reverse("orders:confirmation", args=[order_id])
        res_confirm = self.client.get(confirm_url)
        self.assertEqual(res_confirm.status_code, 200)

    def test_order_status_methods(self):
        # Cas 1: annulation autorisée quand pending
        order_cancel = Order.objects.create(
            user=self.user, offer=self.offer, amount=self.offer.price
        )
        self.assertTrue(order_cancel.can_be_cancelled())
        order_cancel.mark_as_cancelled()
        self.assertEqual(order_cancel.status, "cancelled")

        # Cas 2: paiement puis tentative d'annulation (refusée)
        order_pay = Order.objects.create(
            user=self.user, offer=self.offer, amount=self.offer.price
        )
        self.assertTrue(order_pay.can_be_paid())
        order_pay.mark_as_paid()
        self.assertEqual(order_pay.status, "paid")
        result = order_pay.mark_as_cancelled()
        self.assertFalse(result)
        self.assertEqual(order_pay.status, "paid")


