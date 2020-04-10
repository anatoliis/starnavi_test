from django.utils.decorators import method_decorator
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import mixins, serializers, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet

from social_network.api.serializers.post_like import PostLikeSerializer
from social_network.models import PostLike


@method_decorator(
    name="create",
    decorator=swagger_auto_schema(
        operation_summary="Like Post",
        operation_description="Marks a given Post as liked.",
        request_body=serializers.Serializer,
        responses={
            status.HTTP_201_CREATED: openapi.Response("Created", PostLikeSerializer)
        },
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
    mixins.CreateModelMixin, mixins.DestroyModelMixin, GenericViewSet,
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
        if self.action == "create" and "data" in kwargs:
            kwargs["data"]["post"] = self.kwargs["post_id"]
        return super().get_serializer(*args, **kwargs)
