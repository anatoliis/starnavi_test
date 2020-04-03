from django.utils.decorators import method_decorator
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework_simplejwt.views import TokenRefreshView

from social_network.users.serializers.token_obtain_pair import (
    RetrieveTokenPairSerializer,
)

DecoratedTokenRefreshView = method_decorator(
    name="post",
    decorator=swagger_auto_schema(
        operation_summary="Refresh Token",
        responses={
            status.HTTP_200_OK: openapi.Response("", RetrieveTokenPairSerializer)
        },
    ),
)(TokenRefreshView)
