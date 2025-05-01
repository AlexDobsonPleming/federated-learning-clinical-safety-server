# tests/test_metrics_api.py
import pytest
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from api.models import FlModel

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

@pytest.fixture
def model(db):
    return FlModel.objects.create(
        name="TestModel",
        accuracy=0.95,
        precision=0.90,
        cross_validation=0.92,
        security=0.85,
    )

def test_metrics_requires_authentication(api_client):
    """Unauthenticated list requests get 401."""
    response = api_client.get("/api/models/")
    assert response.status_code == 401

def test_metrics_with_token(api_client, token):
    """Authenticated list requests return 200 and JSON list."""
    api_client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")
    response = api_client.get("/api/models/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

# --- New tests for the detail endpoint ---

def test_get_single_model_requires_authentication(api_client, model):
    """Unauthenticated detail requests get 401."""
    url = f"/api/models/{model.id}/"
    response = api_client.get(url)
    assert response.status_code == 401

def test_get_nonexistent_model_returns_404(api_client, token):
    """Authenticated detail requests for missing IDs get 404."""
    api_client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")
    response = api_client.get("/api/models/9999/")
    assert response.status_code == 404

def test_get_single_model_detail(api_client, token, model):
    """Authenticated detail requests return the correct model data."""
    api_client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")
    url = f"/api/models/{model.id}/"
    response = api_client.get(url)
    assert response.status_code == 200

    data = response.json()
    # Check fields and values
    assert data["id"] == model.id
    assert data["name"] == model.name
    # Use pytest.approx for float comparisons
    assert pytest.approx(data["accuracy"], rel=1e-3) == model.accuracy
    assert pytest.approx(data["precision"], rel=1e-3) == model.precision
    assert pytest.approx(data["cross_validation"], rel=1e-3) == model.cross_validation
    assert pytest.approx(data["security"], rel=1e-3) == model.security
