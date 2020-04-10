from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema
from rest_framework import mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet

from social_network.api.serializers.post_like import PostLikeSerializer
from social_network.models import PostLike


@method_decorator(
    name="retrieve",
    decorator=swagger_auto_schema(
        operation_summary="Check Like",
        operation_description="Returns Like ID and creation date in case given Post is marked as liked.",
    ),
)
@method_decorator(
    name="create",
    decorator=swagger_auto_schema(
        operation_summary="Like Post",
        operation_description="Marks a given Post as liked.",
    ),
)
@method_decorator(
    name="destroy",
    decorator=swagger_auto_schema(
        operation_summary="Unlike Post",
        operation_description="Unmarks a given Post as liked.",
    ),
)
class PostLikeViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    GenericViewSet,
):
    permission_classes = [IsAuthenticated]
    queryset = PostLike.objects.all()
    serializer_class = PostLikeSerializer
    lookup_url_kwarg = "post_id"
    lookup_field = "post_id"

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user=self.request.user)

    def get_serializer(self, *args, **kwargs):
        if self.action == "create":
            kwargs["data"]["post"] = self.kwargs["post_id"]
        return super().get_serializer(*args, **kwargs)
