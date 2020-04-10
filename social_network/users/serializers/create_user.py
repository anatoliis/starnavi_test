from rest_framework import serializers

from social_network.models import User


class CreateUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ("id", "username", "password")

        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        return User.objects.create_user(
            username=validated_data["username"], password=validated_data["password"]
        )
