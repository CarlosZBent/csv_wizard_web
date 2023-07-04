from .models import File
from rest_framework import serializers
from rest_framework.validators import ValidationError


class FileSerializer(serializers.ModelSerializer):

    user = serializers.SlugRelatedField(slug_field=user)
    size = serializers.CharField(max_length=50)
    name = serializers.CharField(max_length=250)
    is_deleted = serializers.BooleanField()
    created_at = serializers.DateTimeField(auto_now_add=True)

    class Meta:
        model = File
        fields = [
            "user",
            "size",
            "name",
            "is_deleted",
            "created_at"
        ]

        def validate(self, attrs):
            size_is_less_than_1GB = int(size) < 1000000
            