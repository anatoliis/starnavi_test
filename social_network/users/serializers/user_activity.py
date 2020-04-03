from typing import Optional

from django.utils import timezone
from rest_framework import serializers

from social_network.models import User
from social_network.models.user import get_user_last_request_timestamp


class UserActivitySerializer(serializers.ModelSerializer):
    last_request = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ("id", "username", "date_joined", "last_login", "last_request")

    def get_last_request(self, user: User) -> Optional[timezone.datetime]:
        return get_user_last_request_timestamp(user)
