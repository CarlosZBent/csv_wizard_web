from django.shortcuts import render
from django.http import FileResponse
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.serializers import ValidationError
from csv_wizard import CSVWizard, CURRENT_PARENT_DIR
import os
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
                size=request.data.get("file1_contents").size,
                name=request.data.get("file1_contents").name,
                is_deleted=False,
            )
            file_entry.save()
            try:
                os.mkdir(f"./results_files/{request.user.username}/")
            except FileExistsError:
                pass
            
            if request.data.get('file2_contents'):
                file_entry2 = File.objects.create(
                    user=request.user,
                    size=request.data.get("file2_contents").size,
                    name=request.data.get("file2_contents").name,
                    is_deleted=False,
                )
                file_entry2.save()
            
            with open(f"./files/{request.user.username}/{request.data.get('file1_contents').name[:-4]}-{request.user.username}.csv", "wb") as file:
                for chunk in request.data.get("file1_contents").chunks():
                    file.write(chunk)
            if request.data.get('file2_contents'):
                with open(f"./files/{request.user.username}/{request.data.get('file2_contents').name[:-4]}-{request.user.username}.csv", "wb") as file:
                    for chunk in request.data.get("file2_contents").chunks():
                        file.write(chunk)

            operation = request.data.get("operation_name")
            user_results_files_folder_path = f"./results_files/{request.user.username}/"
            file1_filesystem_name = f"{request.data.get('file1_contents').name[:-4]}-{request.user.username}"
            if request.data.get('file2_contents'):
                file2_filesystem_name = f"{request.data.get('file2_contents').name[:-4]}-{request.user.username}"

            # process CSV files
            if request.data.get("file1_contents") and not request.data.get("file2_contents"):
            # only file 1 exists

                file1 = CSVWizard(file1_filesystem_name, f"./files/{request.user.username}")
                file1_encoding = file1.get_encoding()
                
                if operation == "slice":
                    try:
                        os.mkdir(f"{user_results_files_folder_path}/slice/")
                    except FileExistsError:
                        pass
                    
                    result = file1.slice()
                    
                    first_half = CSVWizard(f"{file1_filesystem_name}_FIRST_HALF", f"{user_results_files_folder_path}/slice")
                    second_half = CSVWizard(f"{file1_filesystem_name}_SECOND_HALF", f"{user_results_files_folder_path}/slice")
                    
                    first_half.overwrite(result['First_Half'], file1_encoding)
                    second_half.overwrite(result['Second_Half'], file1_encoding)

                    first_half_file = open(f"{user_results_files_folder_path}/slice/{file1_filesystem_name}_FIRST_HALF.csv", "r")
                    first_half_file_instance = FileResponse(first_half_file, filename=f"{file1_filesystem_name}_FIRST_HALF")

                    # return Response(data={"first_half": first_half_file_instance, "encoding":file1_encoding}, status=status.HTTP_200_OK, content_type="file/csv")
            else:
            # there are two files
                pass

            return Response(status=status.HTTP_201_CREATED)
        else:
            print("invalid: ", serializer.errors)
            return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)