from django.utils.decorators import method_decorator
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny

from social_network.models import User
from social_network.users.serializers.create_user import CreateUserSerializer
from social_network.users.serializers.user import UserSerializer


@method_decorator(
    name="post",
    decorator=swagger_auto_schema(
        operation_summary="Sign Up User",
        operation_description=(
            "Takes username and password and creates "
            "a new User if given credentials are valid."
        ),
        responses={
            status.HTTP_201_CREATED: openapi.Response("Created", UserSerializer)
        },
    ),
)
class CreateUserView(CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    serializer_class = CreateUserSerializer
