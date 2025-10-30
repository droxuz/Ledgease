from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Portfolio


class UsersAccountTests(APITestCase):
    def setUp(self):
        self.username = "testuser"
        self.email = "test@example.com"
        self.password = "StrongP@ssw0rd!"
        self.user = User.objects.create_user(
            username=self.username,
            email=self.email,
            password=self.password,
        )

        self.login_url = reverse("token_obtain_pair")
        self.profile_url = reverse("profile")
        self.portfolio_url = reverse("portfolio")
        self.register_url = reverse("register")

    def test_database_connection_user_and_portfolio(self):
        self.assertTrue(User.objects.filter(username=self.username).exists())

        # Create and fetch a Portfolio row( Portofolio is WIP may not be finalized)
        p = Portfolio.objects.create(
            user=self.user,
            asset_name="Stock A",
            quantity=10,
            purchase_price=100.0,
            current_value=110.0,
        )
        self.assertEqual(Portfolio.objects.filter(user=self.user).count(), 1)
        self.assertIn(self.user.username, str(p))

    def test_login_returns_tokens(self):
        resp = self.client.post(
            self.login_url,
            {"username": self.username, "password": self.password},
            format="json",
        )
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertIn("access", resp.data)
        self.assertIn("refresh", resp.data)

    def test_profile_requires_authentication(self):
        resp = self.client.get(self.profile_url)
        # Depending on REST/auth settings, unauth can be 401 or 403
        self.assertIn(resp.status_code, [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN])

    def authenticate(self):
        resp = self.client.post(
            self.login_url,
            {"username": self.username, "password": self.password},
            format="json",
        )
        token = resp.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

    def test_profile_with_jwt(self):
        self.authenticate()
        resp = self.client.get(self.profile_url)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data.get("username"), self.username)
        self.assertEqual(resp.data.get("email"), self.email)

    def test_portfolio_list_for_user(self):
        Portfolio.objects.create(
            user=self.user,
            asset_name="Coin",
            quantity=2.5,
            purchase_price=200.0,
            current_value=180.0,
        )
        Portfolio.objects.create(
            user=self.user,
            asset_name="Stock B",
            quantity=5,
            purchase_price=50.0,
            current_value=60.0,
        )

        self.authenticate()
        resp = self.client.get(self.portfolio_url)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(len(resp.data), 2)
        names = [row.get("asset_name") for row in resp.data]
        self.assertIn("Coin", names)

    def test_register_missing_fields_returns_400(self):
        # Missing required email should produce 400
        resp = self.client.post(
            self.register_url,
            {"username": "newuser", "password": "WeakP@ss1"},
            format="json",
        )
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("email", resp.data)
