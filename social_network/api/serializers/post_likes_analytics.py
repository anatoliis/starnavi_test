from rest_framework import serializers

from social_network.models import PostLike


class PostLikesAnalyticsSerializer(serializers.ModelSerializer):
    likes_count = serializers.IntegerField()
    date = serializers.DateField()

    class Meta:
        model = PostLike
        fields = ("likes_count", "date")
