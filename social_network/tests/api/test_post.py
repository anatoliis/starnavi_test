from django.urls import reverse
from django.utils import timezone
from freezegun import freeze_time
from model_bakery import baker
from rest_framework.test import APIClient

from social_network.models import Post, PostLike, User

URL_POSTS = reverse("api:post-list")


def test_posts__list_existing_posts(
    authorized_client: APIClient, user: User, post: Post
):
    posts = [post, *baker.make(Post, _quantity=4)]
    post.created_at = timezone.now() + timezone.timedelta(hours=1)
    post.save(update_fields=["created_at"])

    resp = authorized_client.get(path=URL_POSTS)

    assert resp.status_code == 200, resp.json()
    assert resp.json()["count"] == len(posts)
    assert {post.id for post in posts} == {
        post["id"] for post in resp.json()["results"]
    }
    assert resp["X-NS-DEBUG-TOTAL-REQUESTS"] == "2"

    latest_post = resp.json()["results"][0]

    assert latest_post["id"] == post.id
    assert latest_post["user"] == str(user.id)
    assert latest_post["content"] == post.content
    assert latest_post["number_of_likes"] == 0


def test_posts__retrieve_existing_post(
    authorized_client: APIClient, user: User, post: Post
):
    likes = baker.make(PostLike, post=post, _quantity=3)

    resp = authorized_client.get(
        path=reverse("api:post-detail", kwargs={"pk": post.id})
    )

    assert resp.status_code == 200, resp.json()
    assert resp.json()["id"] == post.id
    assert resp.json()["user"] == str(user.id)
    assert resp.json()["content"] == post.content
    assert resp.json()["number_of_likes"] == len(likes)
    assert resp["X-NS-DEBUG-TOTAL-REQUESTS"] == "1"


def test_posts__create_new_post(authorized_client: APIClient, user: User):
    initial_number_of_posts = Post.objects.count()

    post_content = "Post content."
    creation_date = timezone.now()

    with freeze_time(creation_date):
        resp = authorized_client.post(path=URL_POSTS, data={"content": post_content})

    assert resp.status_code == 201, resp.json()
    assert resp.json()["content"] == post_content
    assert resp["X-NS-DEBUG-TOTAL-REQUESTS"] == "1"

    assert Post.objects.count() == initial_number_of_posts + 1

    post = Post.objects.get(pk=resp.json()["id"])
    assert post.user == user
    assert post.content == post_content
    assert post.created_at == creation_date


def test_posts__retrieve_non_existing_post(authorized_client: APIClient, user: User):
    resp = authorized_client.get(
        path=reverse("api:post-detail", kwargs={"pk": 999_999_999})
    )

    assert resp.status_code == 404, resp.json()
    assert resp.json() == {"detail": "Not found."}
    assert resp["X-NS-DEBUG-TOTAL-REQUESTS"] == "1"


def test_posts__create_new_post__given_empty_content(
    authorized_client: APIClient, user: User
):
    resp = authorized_client.post(path=URL_POSTS, data={"content": ""})

    assert resp.status_code == 400, resp.json()
    assert resp.json() == {"content": ["This field may not be blank."]}
    assert resp["X-NS-DEBUG-TOTAL-REQUESTS"] == "0"


def test_posts__list_existing_posts__by_unauthorized_user(client: APIClient):
    resp = client.get(path=URL_POSTS)

    assert resp.status_code == 401, resp.json()
    assert resp.json() == {"detail": "Authentication credentials were not provided."}
    assert resp["X-NS-DEBUG-TOTAL-REQUESTS"] == "0"
