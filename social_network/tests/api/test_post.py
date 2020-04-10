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
    # Ordered from latest Post to earliest
    posts = list(reversed([post, *baker.make(Post, _quantity=4)]))

    # Creating Likes by current and other Users for the 5th Post
    baker.make(PostLike, post=posts[0], _quantity=3)
    baker.make(PostLike, post=posts[0], user=user)

    # Creating Like by current User for the 4th Post
    baker.make(PostLike, post=posts[1], user=user)

    # Creating Likes for the 3rd Post
    baker.make(PostLike, post=posts[2], _quantity=1)

    # Creating Likes for the 2nd Post
    baker.make(PostLike, post=posts[3], _quantity=3)

    # The first Post will not have any Likes

    resp = authorized_client.get(path=URL_POSTS)

    assert resp.status_code == 200, resp.json()
    assert resp.json()["count"] == len(posts)

    results = resp.json()["results"]
    assert results[0]["id"] == posts[0].id
    assert results[0]["number_of_likes"] == 4
    assert results[0]["is_liked"] is True

    assert results[1]["id"] == posts[1].id
    assert results[1]["number_of_likes"] == 1
    assert results[1]["is_liked"] is True

    assert results[2]["id"] == posts[2].id
    assert results[2]["number_of_likes"] == 1
    assert results[2]["is_liked"] is False

    assert results[3]["id"] == posts[3].id
    assert results[3]["number_of_likes"] == 3
    assert results[3]["is_liked"] is False

    assert results[4]["id"] == posts[4].id
    assert results[4]["id"] == post.id
    assert results[4]["user"] == str(user.id)
    assert results[4]["content"] == post.content
    assert results[4]["number_of_likes"] == 0
    assert results[4]["is_liked"] is False

    assert resp["X-NS-DEBUG-TOTAL-REQUESTS"] == "2"


def test_posts__retrieve_existing_post(
    authorized_client: APIClient, user: User, post: Post
):
    likes = (
        *baker.make(PostLike, post=post, _quantity=3),
        baker.make(PostLike, post=post, user=user),
    )

    resp = authorized_client.get(
        path=reverse("api:post-detail", kwargs={"pk": post.id})
    )

    assert resp.status_code == 200, resp.json()
    assert resp.json()["id"] == post.id
    assert resp.json()["user"] == str(user.id)
    assert resp.json()["content"] == post.content
    assert resp.json()["number_of_likes"] == len(likes)
    assert resp.json()["is_liked"] is True
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
