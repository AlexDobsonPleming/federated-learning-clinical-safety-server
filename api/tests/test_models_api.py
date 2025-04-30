# tests/test_metrics_api.py
import pytest
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

User = get_user_model()

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def user(db):
    return User.objects.create_user(username="testuser", password="password123")

@pytest.fixture
def token(user):
    token, _ = Token.objects.get_or_create(user=user)
    return token

def test_metrics_requires_authentication(api_client):
    """Unauthenticated requests get 401."""
    response = api_client.get("/api/models/")
    assert response.status_code == 401

def test_metrics_with_token(api_client, token):
    """Authenticated requests return 200 and JSON data."""
    api_client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")
    response = api_client.get("/api/models/")
    assert response.status_code == 200
    data = response.json()
    # further assertions, e.g. data is a list, has expected fields
    assert isinstance(data, list)
