from django.db.models import (
    IntegerField,
    Case,
    Count,
    Q,
    Value,
    When,
)
from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated

from social_network.api.filters import CreatedAtFilterSet
from social_network.api.serializers.post_likes_analytics import (
    PostLikesAnalyticsSerializer,
)
from social_network.models import PostLike


@method_decorator(
    name="get",
    decorator=swagger_auto_schema(
        operation_summary="Likes Analytics",
        operation_description="Returns total number of Likes aggregated by day in a given interval.",
    ),
)
class PostLikesAnalyticsView(ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = PostLike.objects.all()
    serializer_class = PostLikesAnalyticsSerializer
    filterset_class = CreatedAtFilterSet

    def get_queryset(self):
        queryset = super().get_queryset()

        user_id = str(self.request.user.id.hex)

        queryset = (
            queryset.values("created_date")
            .annotate(
                total_likes_count=Count("id"),
                likes_by_current_user=Count(
                    Case(
                        When(Q(user_id=Value(user_id)), then=1),
                        output_field=IntegerField(),
                    )
                ),
            )
            .order_by("created_date")
        )
        return queryset
