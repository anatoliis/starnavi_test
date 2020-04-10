from django.urls import reverse
from rest_framework.test import APIClient

from social_network.models import User
from social_network.tests.conftest import USERNAME, USER_PASSWORD

URL_SIGNUP = reverse("users:signup")


def test_sign_up__given_valid_credentials(db, client: APIClient):
    initial_number_of_users = User.objects.count()

    resp = client.post(
        path=URL_SIGNUP, data={"username": USERNAME, "password": USER_PASSWORD}
    )

    assert resp.status_code == 201, resp.json()
    assert "id" in resp.json()
    assert "username" in resp.json()
    assert resp.json()["username"] == USERNAME
    assert resp["X-NS-DEBUG-TOTAL-REQUESTS"] == "2"

    assert User.objects.count() == initial_number_of_users + 1
    assert User.objects.filter(username=USERNAME).exists()


def test_sign_up__given_duplicated_username(db, client: APIClient, user: User):
    resp = client.post(
        path=URL_SIGNUP, data={"username": user.username, "password": USER_PASSWORD}
    )

    assert resp.status_code == 400, resp.json()
    assert resp.json() == {"username": ["A user with that username already exists."]}
    assert resp["X-NS-DEBUG-TOTAL-REQUESTS"] == "1"
