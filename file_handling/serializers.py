from .models import File
from rest_framework import serializers, status


class FileSerializer(serializers.ModelSerializer):

    file1_contents = serializers.FileField(write_only=True, required=True)
    file2_contents = serializers.FileField(write_only=True, required=False)
    operation_name = serializers.CharField(max_length=20)
    number_of_parts = serializers.IntegerField(required=False)

    class Meta:
        model = File
        fields = [
            "file1_contents",
            "file2_contents",
            "operation_name",
            "number_of_parts"
        ]
