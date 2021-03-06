from rest_framework import serializers

from social_network.models import Post


class PostCreateSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Post
        fields = ("id", "user", "content")


class PostSerializer(serializers.ModelSerializer):
    number_of_likes = serializers.IntegerField(read_only=True)
    is_liked = serializers.BooleanField()

    class Meta:
        model = Post
        fields = ("id", "user", "content", "number_of_likes", "is_liked", "created_at")
