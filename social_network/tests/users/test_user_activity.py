from unittest.mock import patch

import dateutil.parser
from django.urls import reverse
from django.utils import timezone
from rest_framework.test import APIClient

from social_network.models import User

URL_USER_ACTIVITY = reverse("users:activity")
URL_SIGN_UP = reverse("users:signup")
URL_OBTAIN_TOKEN = reverse("users:token_obtain_pair")


def test_user_activity__date_joined(db, authorized_client: APIClient, user: User):
    resp = authorized_client.get(path=URL_USER_ACTIVITY)

    assert resp.status_code == 200, resp.json()
    assert resp.json()["date_joined"]
    assert dateutil.parser.isoparse(resp.json()["date_joined"]) == user.date_joined


def test_user_activity__last_login(authorized_client: APIClient, user: User):
    last_login = timezone.now()
    user.last_login = last_login
    user.save(update_fields=["last_login"])

    resp = authorized_client.get(path=URL_USER_ACTIVITY)

    assert resp.status_code == 200, resp.json()
    assert resp.json()["last_login"]
    assert dateutil.parser.isoparse(resp.json()["last_login"]) == last_login


def test_user_activity__last_request(authorized_client: APIClient, user: User):
    last_request = timezone.now()

    with patch("social_network.models.user.cache.get", return_value=last_request):
        resp = authorized_client.get(path=URL_USER_ACTIVITY)

    assert resp.status_code == 200, resp.json()
    assert resp.json()["last_request"]
    assert dateutil.parser.isoparse(resp.json()["last_request"]) == last_request
