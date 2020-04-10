from django.urls import reverse
from rest_framework.test import APIClient

from social_network.models import User
from social_network.tests.conftest import USER_PASSWORD

URL_TOKEN_OBTAIN = reverse("users:token_obtain_pair")
URL_TOKEN_REFRESH = reverse("users:token_refresh")


def test_refresh_token__given_valid_refresh_token(client: APIClient, user: User):
    resp = client.post(
        path=URL_TOKEN_OBTAIN,
        data={"username": user.username, "password": USER_PASSWORD},
    )

    assert resp.status_code == 200, resp.json()
    assert "access" in resp.json()
    assert "refresh" in resp.json()

    access_token = resp.json()["access"]
    refresh_token = resp.json()["refresh"]

    resp = client.post(path=URL_TOKEN_REFRESH, data={"refresh": refresh_token})

    assert resp.status_code == 200, resp.json()

    new_access_token = resp.json()["access"]
    new_refresh_token = resp.json()["refresh"]

    assert access_token != new_access_token
    assert refresh_token != new_refresh_token

    assert resp["X-NS-DEBUG-TOTAL-REQUESTS"] == "0"


def test_refresh_token__given_invalid_refresh_token(client: APIClient, user: User):
    resp = client.post(path=URL_TOKEN_REFRESH, data={"refresh": "invalid_token"})

    assert resp.status_code == 401, resp.json()
    assert resp.json() == {
        "code": "token_not_valid",
        "detail": "Token is invalid or expired",
    }
    assert resp["X-NS-DEBUG-TOTAL-REQUESTS"] == "0"
