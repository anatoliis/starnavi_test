import pytest
from model_bakery import baker
from rest_framework.test import APIClient

from social_network.models import User, Post

USERNAME = "test_username"
USER_PASSWORD = "test_password"


@pytest.fixture
def client() -> APIClient:
    return APIClient()


@pytest.fixture
def authorized_client(client: APIClient, user: User) -> APIClient:
    client.force_authenticate(user)
    return client


@pytest.fixture
def user(transactional_db):
    user = User.objects.create_user(username=USERNAME, password=USER_PASSWORD)
    return user


@pytest.fixture
def post(user: User):
    return baker.make(Post, user=user)
