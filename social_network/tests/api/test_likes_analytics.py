from random import randrange

from django.urls import reverse
from django.utils import timezone
from freezegun import freeze_time
from model_bakery import baker
from rest_framework.test import APIClient

from social_network.models import PostLike, User

URL_LIKES_ANALYTICS = reverse("api:likes_analytics")


def test_likes_analytics__retrieve(authorized_client: APIClient, user: User):
    date_from = timezone.datetime(year=2020, month=1, day=1)
    date_to = timezone.datetime(year=2020, month=1, day=5)

    # Creating Likes outside the dates interval
    with freeze_time(date_from - timezone.timedelta(hours=1)):
        baker.make(PostLike, _quantity=3)
        baker.make(PostLike, user=user, _quantity=2)

    with freeze_time(date_to + timezone.timedelta(hours=1)):
        baker.make(PostLike, _quantity=3)
        baker.make(PostLike, user=user, _quantity=1)

    # Creating Likes inside the dates interval
    with freeze_time(timezone.datetime(year=2020, month=1, day=1, hour=randrange(24))):
        baker.make(PostLike, _quantity=4)
        baker.make(PostLike, user=user, _quantity=2)

    with freeze_time(timezone.datetime(year=2020, month=1, day=2, hour=randrange(24))):
        baker.make(PostLike, _quantity=7)
        baker.make(PostLike, user=user, _quantity=3)

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
        {"total_likes_count": 6, "likes_by_current_user": 2, "date": "2020-01-01"},
        {"total_likes_count": 10, "likes_by_current_user": 3, "date": "2020-01-02"},
        {"total_likes_count": 3, "likes_by_current_user": 0, "date": "2020-01-03"},
    ]
    assert resp["X-NS-DEBUG-TOTAL-REQUESTS"] == "2"
