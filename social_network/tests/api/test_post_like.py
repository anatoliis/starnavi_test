import dateutil.parser
import pytest
from django.utils import timezone
from freezegun import freeze_time
from model_bakery import baker
from rest_framework.reverse import reverse
from rest_framework.test import APIClient

from social_network.models import User, Post, PostLike


@pytest.fixture
def post_like(user: User, post: Post) -> PostLike:
    return baker.make(PostLike, user=user, post=post)


def get_post_like_url(post_id: int) -> str:
    return reverse("api:post_like", kwargs={"post_id": post_id})


def test_like__retrieve(authorized_client: APIClient, post_like: PostLike):
    resp = authorized_client.get(path=get_post_like_url(post_id=post_like.post_id))

    assert resp.status_code == 200, resp.json()
    assert resp.json()["id"] == post_like.pk
    assert resp.json()["created_at"]
    assert dateutil.parser.isoparse(resp.json()["created_at"]) == post_like.created_at
    assert resp["X-NS-DEBUG-TOTAL-REQUESTS"] == "1"


def test_likes__create(authorized_client: APIClient, user: User, post: Post):
    initial_number_of_likes = PostLike.objects.count()
    creation_date = timezone.now()

    with freeze_time(creation_date):
        resp = authorized_client.post(path=get_post_like_url(post_id=post.pk))

    assert resp.status_code == 201, resp.json()
    assert resp["X-NS-DEBUG-TOTAL-REQUESTS"] == "3"

    assert PostLike.objects.count() == initial_number_of_likes + 1

    post_like = PostLike.objects.get(pk=resp.json()["id"])

    assert post_like.user_id == user.pk
    assert post_like.post_id == post.pk
    assert post_like.created_at == creation_date


def test_like__remove(authorized_client: APIClient, post_like: PostLike):
    initial_number_of_likes = PostLike.objects.count()
    resp = authorized_client.delete(path=get_post_like_url(post_id=post_like.post_id))

    assert resp.status_code == 204, resp.json()
    assert resp["X-NS-DEBUG-TOTAL-REQUESTS"] == "2"

    assert PostLike.objects.count() == initial_number_of_likes - 1

    with pytest.raises(PostLike.DoesNotExist):
        post_like.refresh_from_db()


def test_like__retrieve_non_existent_like(authorized_client: APIClient, post: Post):
    resp = authorized_client.get(path=get_post_like_url(post_id=post.pk))

    assert resp.status_code == 404, resp.json()
    assert resp.json() == {"detail": "Not found."}
    assert resp["X-NS-DEBUG-TOTAL-REQUESTS"] == "1"


def test_like__retrieve_like_of_non_existent_post(authorized_client: APIClient):
    resp = authorized_client.get(path=get_post_like_url(post_id=999_999_999))

    assert resp.status_code == 404, resp.json()
    assert resp.json() == {"detail": "Not found."}
    assert resp["X-NS-DEBUG-TOTAL-REQUESTS"] == "1"


def test_likes__create_duplicated_like(
    authorized_client: APIClient, post_like: PostLike
):
    resp = authorized_client.post(path=get_post_like_url(post_id=post_like.post_id))

    assert resp.status_code == 400, resp.json()
    assert resp.json() == {"non_field_errors": ["Post already liked."]}
    assert resp["X-NS-DEBUG-TOTAL-REQUESTS"] == "2"


def test_like__create_for_non_existent_post(authorized_client: APIClient):
    resp = authorized_client.post(path=get_post_like_url(post_id=999_999_999))

    assert resp.status_code == 400, resp.json()
    assert resp.json() == {"post": ["Post with given ID does not exist."]}
    assert resp["X-NS-DEBUG-TOTAL-REQUESTS"] == "1"


def test_like__create_by_unauthorized_user(client: APIClient, post: Post):
    resp = client.post(path=get_post_like_url(post_id=post.pk))

    assert resp.status_code == 401, resp.json()
    assert resp.json() == {"detail": "Authentication credentials were not provided."}
    assert resp["X-NS-DEBUG-TOTAL-REQUESTS"] == "0"


def test_like__remove_non_existent_like(authorized_client: APIClient, post: Post):
    initial_number_of_likes = PostLike.objects.count()
    resp = authorized_client.delete(path=get_post_like_url(post_id=post.pk))

    assert resp.status_code == 404, resp.json()
    assert resp.json() == {"detail": "Not found."}
    assert PostLike.objects.count() == initial_number_of_likes
    assert resp["X-NS-DEBUG-TOTAL-REQUESTS"] == "1"


def test_like__remove_from_non_existent_post(authorized_client: APIClient):
    initial_number_of_likes = PostLike.objects.count()
    resp = authorized_client.delete(path=get_post_like_url(post_id=999_999_999))

    assert resp.status_code == 404, resp.json()
    assert resp.json() == {"detail": "Not found."}
    assert PostLike.objects.count() == initial_number_of_likes
    assert resp["X-NS-DEBUG-TOTAL-REQUESTS"] == "1"
