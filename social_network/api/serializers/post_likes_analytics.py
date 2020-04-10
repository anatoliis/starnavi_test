from rest_framework import serializers

from social_network.models import PostLike


class PostLikesAnalyticsSerializer(serializers.ModelSerializer):
    total_likes_count = serializers.IntegerField()
    likes_by_current_user = serializers.IntegerField()
    date = serializers.DateField()

    class Meta:
        model = PostLike
        fields = ("total_likes_count", "likes_by_current_user", "date")
