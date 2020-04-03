from rest_framework import serializers, validators

from social_network.models import PostLike


class PostLikeSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = PostLike
        fields = ("id", "post", "user", "created_at")

        extra_kwargs = {
            "created_at": {"read_only": True},
            "post": {
                "error_messages": {
                    "does_not_exist": "Post with given ID does not exist."
                },
            },
        }

        validators = [
            validators.UniqueTogetherValidator(
                queryset=PostLike.objects.all(),
                fields=("post", "user"),
                message="Post already liked.",
            )
        ]
