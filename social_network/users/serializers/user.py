from rest_framework import serializers

from social_network.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "date_joined")
