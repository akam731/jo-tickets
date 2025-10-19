from django.test import TestCase
from decimal import Decimal
from apps.catalog.models import Offer


class OfferModelTest(TestCase):

    def setUp(self):
        self.offer_data = {
            "name": "solo",
            "capacity": 1,
            "price": Decimal("50.00"),
            "description": "Test offer",
            "is_active": True,
        }

    def test_offer_creation(self):
        offer = Offer.objects.create(**self.offer_data)

        self.assertEqual(offer.name, "solo")
        self.assertEqual(offer.capacity, 1)
        self.assertEqual(offer.price, Decimal("50.00"))
        self.assertEqual(offer.description, "Test offer")
        self.assertTrue(offer.is_active)

    def test_offer_str_representation(self):
        offer = Offer.objects.create(**self.offer_data)
        expected = "Solo - 50.00€ (1 personne)"
        self.assertEqual(str(offer), expected)

    def test_get_capacity_display(self):
        offer = Offer.objects.create(**self.offer_data)
        self.assertEqual(offer.get_capacity_display(), "1 personne")

        offer.capacity = 4
        self.assertEqual(offer.get_capacity_display(), "4 personnes")

    def test_is_available(self):
        offer = Offer.objects.create(**self.offer_data)
        self.assertTrue(offer.is_available())

        offer.is_active = False
        offer.save()
        self.assertFalse(offer.is_available())

    def test_offer_choices(self):
        valid_choices = [choice[0] for choice in Offer.OFFER_TYPES]
        self.assertIn("solo", valid_choices)
        self.assertIn("duo", valid_choices)
        self.assertIn("familiale", valid_choices)

    def test_price_validation(self):
        with self.assertRaises(Exception):
            Offer.objects.create(
                name="test",
                capacity=1,
                price=Decimal("0.00"),
                is_active=True,
            )

    def test_offer_ordering(self):
        Offer.objects.create(
            name="duo", capacity=2, price=Decimal("90.00"), is_active=True
        )
        Offer.objects.create(
            name="familiale", capacity=4, price=Decimal("160.00"), is_active=True
        )
        Offer.objects.create(**self.offer_data)

        offers = Offer.objects.all()
        self.assertEqual(offers[0].name, "solo")
        self.assertEqual(offers[1].name, "duo")
        self.assertEqual(offers[2].name, "familiale")

    def test_offer_uniqueness(self):
        Offer.objects.create(**self.offer_data)

        with self.assertRaises(Exception):
            Offer.objects.create(
                name="solo",
                capacity=2,
                price=Decimal("100.00"),
                is_active=True,
            )
