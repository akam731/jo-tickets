from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model


User = get_user_model()


class ControlAccessTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.scan_url = reverse("control:scan")

    def test_scan_requires_employee(self):
        # Utilisateur normal
        user = User.objects.create_user(
            email="user@example.com",
            username="user",
            first_name="User",
            last_name="Normal",
            password="MotDePasse123!",
        )
        self.client.force_login(user)
        res = self.client.get(self.scan_url)
        self.assertIn(res.status_code, [302, 403])

        # Employé
        employee = User.objects.create_user(
            email="emp@example.com",
            username="emp",
            first_name="Emp",
            last_name="Loyee",
            password="MotDePasse123!",
            is_employee=True,
        )
        self.client.force_login(employee)
        res_ok = self.client.get(self.scan_url)
        self.assertEqual(res_ok.status_code, 200)


