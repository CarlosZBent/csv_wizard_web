from .models import File
from rest_framework import serializers, status
from rest_framework.validators import ValidationError


class FileSerializer(serializers.ModelSerializer):

    name = serializers.CharField(max_length=250)
    size = serializers.FloatField(required=True)
    file1_contents = serializers.FileField(write_only=True, required=True)
    file2_contents = serializers.FileField(write_only=True, required=False)
    operation_name = serializers.CharField(max_length=15)
    number_of_parts = serializers.IntegerField(required=False)

    class Meta:
        model = File
        fields = [
            "name",
            "size",
            "file1_contents",
            "file2_contents",
            "operation_name",
            "number_of_parts"
        ]

        def validate(self, attrs):

            available_operations = [
                "slice",
                "divide",
                "find_common_rows",
                "find_different_rows",
                "get_duplicates"
            ]

            operation_name = attrs.get("operation_name")
            number_of_parts = attrs.get("number_of_parts")
            file2_contents = attrs.get("file2_contents")
            
            if not operation_name in available_operations:
                print("wrong opp")
                raise ValidationError("Invalid Operation Name", status.HTTP_400_BAD_REQUEST)
            
            if operation_name == "divide" and not number_of_parts:
                print("no number of parts")
                raise ValidationError("Operation is 'divide' but no number of parts was provided", status.HTTP_400_BAD_REQUEST)

            if operation_name == "find_common_rows" or operation_name == "find_different_rows":
                if not file2_contents:
                    print("needs 2 files")
                    raise ValidationError("Operations 'find_common_rows' and 'find_different_rows' require TWO files", status.HTTP_400_BAD_REQUEST)

            if "(text/csv)" not in attrs.get("file1_contents"):
                print("file1 is not csv")
                raise ValidationError("File 1 is not a CSV", status.HTTP_400_BAD_REQUEST)
            
            if file2_contents:
                if "(text/csv)" not in file2_contents:
                    print("file2 is not csv")
                    raise ValidationError("File 2 is not a CSV", status.HTTP_400_BAD_REQUEST)

            return super().validate(attrs)


