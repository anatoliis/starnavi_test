from rest_framework_simplejwt.authentication import JWTAuthentication

from social_network.models.user import update_user_last_request_timestamp


class Authentication(JWTAuthentication):
    def get_user(self, validated_token):
        user = super().get_user(validated_token)
        update_user_last_request_timestamp(user)
        return user
