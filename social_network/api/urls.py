from django.urls import path
from rest_framework.routers import DefaultRouter

from social_network.api.views.likes_analytics import PostLikesAnalyticsView
from social_network.api.views.post import PostViewSet
from social_network.api.views.post_like import PostLikeViewSet

app_name = "social_network"

router = DefaultRouter()
router.register("posts", PostViewSet, basename="post")

urlpatterns = [
    path(
        "posts/<int:post_id>/like/",
        PostLikeViewSet.as_view(actions={"post": "create", "delete": "destroy"}),
        name="post_like",
    ),
    path("analytics/", PostLikesAnalyticsView.as_view(), name="likes_analytics"),
]

urlpatterns += router.urls
