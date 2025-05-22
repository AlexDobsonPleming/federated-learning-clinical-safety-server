# api/tests/test_auth_token.py
from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from django.urls import reverse

class AuthTokenTests(APITestCase):
    def setUp(self):
        self.username = 'testuser'
        self.password = 'secret123'
        # Create a user for authentication
        self.user = User.objects.create_user(username=self.username, password=self.password)
        # URL for the DRF token auth endpoint
        self.url = reverse('api-token-auth')  # routes to "/api/auth/token/"

    def test_obtain_token_success(self):
        """
        Valid credentials should return HTTP 200 and a token in the response.
        """
        response = self.client.post(
            self.url,
            {'username': self.username, 'password': self.password},
            format='json'
        )
        # Check for success
        self.assertEqual(response.status_code, 200)
        self.assertIn('token', response.data)
        token_key = response.data['token']
        # Verify that the token exists in the database
        self.assertTrue(Token.objects.filter(user=self.user, key=token_key).exists())

    def test_obtain_token_invalid_credentials(self):
        """
        Invalid credentials should return HTTP 400 with non_field_errors.
        """
        response = self.client.post(
            self.url,
            {'username': self.username, 'password': 'wrongpass'},
            format='json'
        )
        self.assertEqual(response.status_code, 400)
        # DRF returns non_field_errors on credential mismatch
        self.assertIn('non_field_errors', response.data)

    def test_obtain_token_missing_fields(self):
        """
        Missing username/password fields should return HTTP 400 with field errors.
        """
        response = self.client.post(self.url, {}, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertIn('username', response.data)
        self.assertIn('password', response.data)
