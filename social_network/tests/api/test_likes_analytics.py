from random import randrange

from django.urls import reverse
from django.utils import timezone
from freezegun import freeze_time
from model_bakery import baker
from rest_framework.test import APIClient

from social_network.models import PostLike

URL_LIKES_ANALYTICS = reverse("api:likes_analytics")


def test_likes_analytics__retrieve(authorized_client: APIClient):
    date_from = timezone.datetime(year=2020, month=1, day=1)
    date_to = timezone.datetime(year=2020, month=1, day=5)

    # Creating Likes outside the dates interval
    with freeze_time(date_from - timezone.timedelta(hours=1)):
        baker.make(PostLike, _quantity=3)

    with freeze_time(date_to + timezone.timedelta(hours=1)):
        baker.make(PostLike, _quantity=3)

    # Creating Likes inside the dates interval
    with freeze_time(timezone.datetime(year=2020, month=1, day=1, hour=randrange(24))):
        baker.make(PostLike, _quantity=4)

    with freeze_time(timezone.datetime(year=2020, month=1, day=2, hour=randrange(24))):
        baker.make(PostLike, _quantity=7)

    with freeze_time(timezone.datetime(year=2020, month=1, day=3, hour=randrange(24))):
        baker.make(PostLike, _quantity=3)

    resp = authorized_client.get(
        path=URL_LIKES_ANALYTICS,
        data={
            "date_from": date_from.date().isoformat(),
            "date_to": date_to.date().isoformat(),
        },
    )

    assert resp.status_code == 200, resp.json()
    assert resp.json()["count"] == 3
    assert resp.json()["results"] == [
        {"likes_count": 4, "date": "2020-01-01"},
        {"likes_count": 7, "date": "2020-01-02"},
        {"likes_count": 3, "date": "2020-01-03"},
    ]
