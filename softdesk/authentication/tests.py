from rest_framework.test import APITestCase
from django.urls import reverse_lazy
from rest_framework import status

from authentication.models import User


class TestUser(APITestCase):

    url = reverse_lazy("users-list")

    def test_list(self):
        number_user = User.objects.count()
        User.objects.create(username="flo", date_of_birth="2000-01-01")
        User.objects.create(username="Achille", date_of_birth="2005-01-01")

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["count"], number_user + 2)

    def test_create_user_underage(self):
        self.assertFalse(User.objects.exists())
        response = self.client.post(self.url, data={"username": "Tentative", "date_of_birth": "2015-01-01"})
        self.assertEqual(response.status_code, 400)
        self.assertFalse(User.objects.filter(username="Tentative").exists())


class TestUserUpdate(APITestCase):
    def setUp(self):
        self.user = User.objects.create(username="user1", date_of_birth="2000-01-01")
        self.client.force_authenticate(user=self.user)

    def test_update_user(self):
        url = reverse_lazy("users-detail", kwargs={"pk": self.user.pk})
        response = self.client.patch(url, data={"username": "updateduser"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertEqual(self.user.username, "updateduser")


class TestUserDelete(APITestCase):
    def setUp(self):
        self.user = User.objects.create(username="user1", date_of_birth="2000-01-01")
        self.client.force_authenticate(user=self.user)

    def test_delete_user(self):
        url = reverse_lazy("users-detail", kwargs={"pk": self.user.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204)
