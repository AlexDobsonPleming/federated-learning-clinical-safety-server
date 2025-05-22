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
def machine_user(db):
    u = User.objects.create(username="uploader1")
    u.set_unusable_password()
    u.save()
    return u

@pytest.fixture
def machine_token(machine_user):
    token, _ = Token.objects.get_or_create(user=machine_user)
    return token

@pytest.fixture
def model(db):
    return FlModel.objects.create(
        name="TestModel",
        accuracy=0.95,
        generalisability=0.90,
        privacy=0.85,
    )
