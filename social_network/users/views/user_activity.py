from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema
from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import IsAuthenticated

from social_network.users.serializers.user_activity import UserActivitySerializer


@method_decorator(
    name="get",
    decorator=swagger_auto_schema(
        operation_summary="User Activity",
        operation_description="Returns current User's activity information.",
    ),
)
class UserActivityView(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserActivitySerializer

    def get_object(self):
        return self.request.user
