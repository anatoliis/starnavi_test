import pytest
from django.urls import reverse
from django.utils import timezone
from freezegun import freeze_time
from rest_framework.test import APIClient

from social_network.models import User
from social_network.tests.conftest import USER_PASSWORD, USERNAME

URL_TOKEN_OBTAIN = reverse("users:token_obtain_pair")


@pytest.mark.parametrize("username", [USERNAME, f" {USERNAME} "])
def test_obtain_token__given_valid_credentials(
    db, client: APIClient, user: User, username: str
):
    last_login = timezone.now()

    with freeze_time(last_login):
        resp = client.post(
            path=URL_TOKEN_OBTAIN,
            data={"username": username, "password": USER_PASSWORD},
        )

    assert resp.status_code == 200, resp.json()
    assert "access" in resp.json()
    assert "refresh" in resp.json()

    user.refresh_from_db()

    assert user.last_login == last_login


@pytest.mark.parametrize(
    "username, password",
    [
        ("invalid_username", "invalid_password"),
        (USER_PASSWORD, "invalid_password"),
        ("invalid_username", USER_PASSWORD),
    ],
)
def test_obtain_token__given_invalid_credentials(
    db, client: APIClient, username: str, password: str
):
    resp = client.post(
        path=URL_TOKEN_OBTAIN, data={"username": username, "password": password}
    )

    assert resp.status_code == 401, resp.json()
    assert resp.json()["detail"] == "No active account found with the given credentials"
