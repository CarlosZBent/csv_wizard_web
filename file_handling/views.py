from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.serializers import ValidationError
from . import serializers
from .models import File


available_operations = [
    "slice",
    "divide",
    "find_common_rows",
    "find_different_rows",
    "get_duplicates"
]

class FilesView(generics.GenericAPIView):
    
    serializer_class = serializers.FileSerializer

    def get_queryset(self):
        return self.request
    

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            # after DRF default validation, apply other custom validations
            if request.data.get("operation_name") not in available_operations:
                raise ValidationError({"operation_error":"operation does not exist"}, status.HTTP_400_BAD_REQUEST)
            if request.data.get("operation_name") == "divide" and not request.data.get("number_of_parts"):
                raise ValidationError({"number_of_parts_error":"operation 'divide' needs a specific number of parts"}, status.HTTP_400_BAD_REQUEST)
            if request.data.get("operation_name") == "find_common_rows" or request.data.get("operation_name") == "find_different_rows":
                if not request.data.get("file2_contents"):
                    raise ValidationError({"amount_of_files_error":"Operations 'find_common_rows' and 'find_different_rows' require TWO files"}, status.HTTP_400_BAD_REQUEST)
            if request.data.get("file1_contents").content_type != "text/csv":
                raise ValidationError({"file_type_error":"File 1 is not a CSV"}, status.HTTP_400_BAD_REQUEST)
            if request.data.get("file2_contents"):
                if request.data.get("file2_contents").content_type != "text/csv":
                    raise ValidationError({"file_type_error":"File 2 is not a CSV"}, status.HTTP_400_BAD_REQUEST)

            file_entry = File.objects.create(
                user=request.user,
                size=request.data.get("size"),
                name=request.data.get("name"),
                is_deleted=False,
            )
            file_entry.save()
            return Response(status=status.HTTP_201_CREATED)
        else:
            print("invalid: ", serializer.errors)
            return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)