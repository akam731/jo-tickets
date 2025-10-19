from django.test import TestCase, Client
from django.urls import reverse


class ErrorHandlersTest(TestCase):

    def setUp(self):
        self.client = Client()

    def test_error_pages(self):
        for code in [400, 403, 404, 500]:
            url = reverse("test_error", args=[str(code)])
            res = self.client.get(url)
            self.assertEqual(res.status_code, code)


