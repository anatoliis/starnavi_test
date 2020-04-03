from django.contrib.auth.signals import user_logged_in
from django.utils.decorators import method_decorator
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from rest_framework_simplejwt.views import TokenObtainPairView

from social_network.models import User
from social_network.users.serializers.token_obtain_pair import (
    RetrieveTokenPairSerializer,
)


@method_decorator(
    name="post",
    decorator=swagger_auto_schema(
        operation_summary="Obtain Token Pair",
        operation_description=(
            "Takes username and password and returns an access and "
            "refresh type JSON web tokens if given User credentials are valid."
        ),
        responses={
            status.HTTP_200_OK: openapi.Response("", RetrieveTokenPairSerializer)
        },
    ),
)
class ObtainTokenView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])

        user_logged_in.send(sender=User, request=request, user=serializer.user)

        return Response(serializer.validated_data, status=status.HTTP_200_OK)
