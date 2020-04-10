from django.db.models import Count
from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema
from rest_framework import mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet

from social_network.api.serializers.post import PostCreateSerializer, PostSerializer
from social_network.models import Post


@method_decorator(
    name="create",
    decorator=swagger_auto_schema(
        operation_summary="Create New Post",
        operation_description="Creates new Post authored by current User.",
    ),
)
@method_decorator(
    name="list",
    decorator=swagger_auto_schema(
        operation_summary="List Posts",
        operation_description="Returns paginated list of all available Posts.",
    ),
)
@method_decorator(
    name="retrieve",
    decorator=swagger_auto_schema(
        operation_summary="Retrieve Post",
        operation_description="Takes Post ID and returns its details.",
    ),
)
class PostViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    GenericViewSet,
):
    permission_classes = [IsAuthenticated]
    queryset = Post.objects.annotate(number_of_likes=Count("likes"))
    serializer_class = PostSerializer

    def get_serializer_class(self):
        if self.action == "create":
            return PostCreateSerializer
        return super().get_serializer_class()
