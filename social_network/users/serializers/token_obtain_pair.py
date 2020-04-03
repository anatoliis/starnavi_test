from rest_framework import serializers


class RetrieveTokenPairSerializer(serializers.Serializer):
    access = serializers.CharField()
    refresh = serializers.CharField(required=False)
