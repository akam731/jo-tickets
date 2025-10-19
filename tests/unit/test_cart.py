from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from unittest.mock import patch
import json

from apps.catalog.models import Offer
from apps.cart.models import Cart, CartItem


User = get_user_model()


class CartApiTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            email="buyer@example.com",
            username="buyer",
            first_name="Buyer",
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

        self.add_url = reverse("cart:add_to_cart")
        self.update_qty_url = reverse("cart:update_quantity_ajax")
        self.remove_item_url = reverse("cart:remove_item_ajax")
        self.checkout_url = reverse("cart:checkout")
        self.pay_url = reverse("cart:process_payment")

    def test_add_to_cart_and_increment(self):
        payload = {"offer_id": self.offer.id, "quantity": 1}
        res1 = self.client.post(
            self.add_url,
            data=json.dumps(payload),
            content_type="application/json",
        )
        self.assertEqual(res1.status_code, 200)
        self.assertTrue(res1.json().get("success"))
        self.assertEqual(Cart.objects.get(user=self.user).total_items, 1)

        # Ajout de la même offre -> incrémente
        res2 = self.client.post(
            self.add_url,
            data=json.dumps(payload),
            content_type="application/json",
        )
        self.assertEqual(res2.status_code, 200)
        self.assertTrue(res2.json().get("success"))
        self.assertEqual(Cart.objects.get(user=self.user).total_items, 2)

    def test_update_quantity_and_remove(self):
        # Préparer un item
        cart, _ = Cart.objects.get_or_create(user=self.user)
        item = CartItem.objects.create(cart=cart, offer=self.offer, quantity=2)

        # Mettre quantité à 3
        res = self.client.post(
            self.update_qty_url,
            data=json.dumps({"item_id": item.id, "quantity": 3}),
            content_type="application/json",
        )
        self.assertEqual(res.status_code, 200)
        item.refresh_from_db()
        self.assertEqual(item.quantity, 3)

        # Mettre quantité à 0 -> suppression
        res = self.client.post(
            self.update_qty_url,
            data=json.dumps({"item_id": item.id, "quantity": 0}),
            content_type="application/json",
        )
        self.assertEqual(res.status_code, 200)
        self.assertFalse(CartItem.objects.filter(id=item.id).exists())

    def test_remove_item_ajax(self):
        cart, _ = Cart.objects.get_or_create(user=self.user)
        item = CartItem.objects.create(cart=cart, offer=self.offer, quantity=1)

        res = self.client.post(
            self.remove_item_url,
            data=json.dumps({"item_id": item.id}),
            content_type="application/json",
        )
        self.assertEqual(res.status_code, 200)
        self.assertTrue(res.json().get("success"))
        self.assertFalse(CartItem.objects.filter(id=item.id).exists())

    @patch("time.sleep", return_value=None)
    def test_checkout_and_payment_flow(self, _sleep):
        # Ajouter 2 items
        self.client.post(
            self.add_url,
            data=json.dumps({"offer_id": self.offer.id, "quantity": 2}),
            content_type="application/json",
        )

        # Accès checkout OK
        res_checkout = self.client.get(self.checkout_url)
        self.assertEqual(res_checkout.status_code, 200)

        # Paiement
        res_pay = self.client.post(
            self.pay_url,
            data=json.dumps({
                "payment_method": "card",
                "card_number": "4111 1111 1111 1111",
            }),
            content_type="application/json",
        )
        self.assertEqual(res_pay.status_code, 200)
        data = res_pay.json()
        self.assertTrue(data.get("success"))
        self.assertIn("orders", data)
        self.assertEqual(len(data.get("orders")), 2)
        # Panier vidé
        self.assertEqual(Cart.objects.get(user=self.user).items.count(), 0)


class CartPaymentEdgesTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            email="edge@example.com",
            username="edge",
            first_name="Edge",
            last_name="Case",
            password="MotDePasse123!",
        )
        self.client.force_login(self.user)

        self.offer = Offer.objects.create(
            name="familiale",
            capacity=4,
            price="40.00",
            description="Offre familiale",
            is_active=True,
        )

        self.add_url = reverse("cart:add_to_cart")
        self.pay_url = reverse("cart:process_payment")

    def test_payment_invalid_method(self):
        res = self.client.get(self.pay_url)
        self.assertIn(res.status_code, [405, 302])

    def test_payment_invalid_method_type(self):
        # Méthode inconnue
        res = self.client.post(
            self.pay_url,
            data=json.dumps({"payment_method": "bitcoin"}),
            content_type="application/json",
        )
        self.assertEqual(res.status_code, 200)
        self.assertFalse(res.json().get("success"))

    def test_payment_invalid_card_number(self):
        # Ajouter un item pour éviter le cas panier vide
        self.client.post(
            self.add_url,
            data=json.dumps({"offer_id": self.offer.id, "quantity": 1}),
            content_type="application/json",
        )
        res = self.client.post(
            self.pay_url,
            data=json.dumps({
                "payment_method": "card",
                "card_number": "1234",  # trop court
            }),
            content_type="application/json",
        )
        self.assertEqual(res.status_code, 200)
        self.assertFalse(res.json().get("success"))

    def test_payment_empty_cart(self):
        res = self.client.post(
            self.pay_url,
            data=json.dumps({"payment_method": "paypal"}),
            content_type="application/json",
        )
        self.assertEqual(res.status_code, 200)
        self.assertFalse(res.json().get("success"))

    def test_payment_paypal_success(self):
        # Ajouter 1 item
        self.client.post(
            self.add_url,
            data=json.dumps({"offer_id": self.offer.id, "quantity": 1}),
            content_type="application/json",
        )
        res = self.client.post(
            self.pay_url,
            data=json.dumps({"payment_method": "paypal"}),
            content_type="application/json",
        )
        self.assertEqual(res.status_code, 200)
        self.assertTrue(res.json().get("success"))
        # Panier vidé
        self.assertEqual(Cart.objects.get(user=self.user).items.count(), 0)


