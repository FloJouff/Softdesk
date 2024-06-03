from rest_framework.test import APITestCase
from django.urls import reverse_lazy

from authentication.models import User


class TestUser(APITestCase):

    url = reverse_lazy("users-list")

    def format_datetime(self, value):
        return value.strftime("%Y-%m-%dT%H:%M:%S.%fZ")

    def test_list(self):
        user = User.objects.create(username="flo", date_of_birth="2000-01-01")
        User.objects.create(username="Achille", date_of_birth="2020-01-01")

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

        expected = [
            {
                "username": user.username,
                "date_of_birth": str(user.date_of_birth),
                "can_be_contacted": user.can_be_contacted,
                "can_data_be_shared": user.can_data_be_shared,
                "created_time": self.format_datetime(user.created_time),
            }
        ]
        self.assertEqual(response.json(), expected)

    def test_create(self):
        self.assertFalse(User.objects.exists())
        response = self.client.post(self.url, data={"username": "Tentative"})
        self.assertEqual(response.status_code, 400)
        self.assertFalse(User.objects.exists())
