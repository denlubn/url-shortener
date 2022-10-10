from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status

from rest_framework.test import APIClient

from url_shortener.models import URL

LIST_URL = reverse("url_shortener:url-list")


def sample_url(user_id: int, short_url: str = "astley"):
    defaults = {
        "original_link": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
        "short_url": f"/{short_url}",
        "user_id": user_id
    }
    return URL.objects.create(**defaults)


class UnauthenticatedUrlShortenerApiTests(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()

    def test_redirect(self):
        user1 = get_user_model().objects.create_user(
            "test@test.com",
            "testpass",
        )
        url = sample_url(user1.id)
        res = self.client.get(url.short_url)

        self.assertEqual(res.status_code, 301)

    def test_auth_required(self):
        res = self.client.get(LIST_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedUrlShortenerApiTests(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "test@test.com",
            "testpass",
        )
        self.client.force_authenticate(self.user)

    def test_create_short_urls(self):
        payload = {
            "original_link": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
        }
        res = self.client.post(LIST_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertIn("short_url", res.data)

    def test_list_not_admin_user(self):
        user2 = get_user_model().objects.create_user(
            "user2@test.com",
            "user2password",
        )
        sample_url(user2.id, "ed5rr")
        sample_url(self.user.id, "85frt")

        res = self.client.get(LIST_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data["count"], 1)


class AdminUrlShortenerApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_superuser(
            "admin@admin.com", "testpass"
        )
        self.client.force_authenticate(self.user)

    def test_list_admin_user(self):
        user2 = get_user_model().objects.create_user(
            "user2@test.com",
            "user2password",
        )
        sample_url(user2.id, "ed5rr")
        sample_url(self.user.id, "85frt")

        res = self.client.get(LIST_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data["count"], 2)
