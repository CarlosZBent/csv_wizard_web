from django.shortcuts import render
from django.http import HttpResponse
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
    "delete_blanks",
    "find_common_rows",
    "find_different_rows"
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
                    
                    try:
                        result = file1.slice()
                        
                        first_half = CSVWizard(f"{file1_filesystem_name}_FIRST_HALF", f"{user_results_files_folder_path}/slice")
                        second_half = CSVWizard(f"{file1_filesystem_name}_SECOND_HALF", f"{user_results_files_folder_path}/slice")
                        
                        first_half.overwrite(result['First_Half'], file1_encoding)
                        second_half.overwrite(result['Second_Half'], file1_encoding)

                        return Response(data={
                            "operation": "slice", 
                            "filename": {
                                "first_half": f"{file1_filesystem_name}_FIRST_HALF",
                                "second_half": f"{file1_filesystem_name}_SECOND_HALF"
                            }}, 
                            status=status.HTTP_200_OK)
                    except Exception as e:
                        return Response(data={"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

                elif operation == "divide":

                    number_of_parts = int(request.data.get('number_of_parts'))
                    
                    try:
                        os.mkdir(f"{user_results_files_folder_path}/divide/")
                    except FileExistsError:
                        pass

                    try:
                        result = file1.divide(number_of_parts)

                        for i in range(number_of_parts):
                            part = CSVWizard(f"{file1_filesystem_name}-divided_part_{i + 1}", f"{user_results_files_folder_path}/divide/")
                            part.overwrite(result[i], file1_encoding)

                        return Response(data={"download_links":"DUMMY_LINKS"}, status=status.HTTP_200_OK)
                    except Exception as e:
                        return Response(data={"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

                elif operation == "delete_blanks":

                    try:
                        os.mkdir(f"{user_results_files_folder_path}/delete_blanks/")
                    except FileExistsError:
                        pass
                    
                    try:
                        result = file1.delete_blanks()

                        no_blanks_file = CSVWizard(f"{file1_filesystem_name}_no_blanks", f"{user_results_files_folder_path}/delete_blanks/")
                        no_blanks_file.overwrite(result, file1_encoding)

                        return Response(data={"download_link":"DUMMY_LINK"}, status=status.HTTP_200_OK)
                        
                    except Exception as e:
                        return Response(data={"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

            elif request.data.get("file1_contents") and request.data.get("file2_contents"):
            # there are two files

                file1 = CSVWizard(file1_filesystem_name, f"./files/{request.user.username}")
                file1_encoding = file1.get_encoding()
                file2 = CSVWizard(file2_filesystem_name, f"./files/{request.user.username}")
                file2_encoding = file2.get_encoding()

                if operation == "find_common_rows":
                    
                    try:
                        os.mkdir(f"{user_results_files_folder_path}/find_common_rows/")
                    except FileExistsError:
                        pass

                    try:
                        result = file1.find_common_rows(file2)

                        common_rows_file = CSVWizard(f"{file1_filesystem_name}-{file2_filesystem_name}_common_rows", f"{user_results_files_folder_path}/find_common_rows/")
                        common_rows_file.overwrite(result, file1_encoding)

                        return Response(data={"download_link":"DUMMY_LINK"}, status=status.HTTP_200_OK)
                    except Exception as e:
                        return Response(data={"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

                elif operation == "find_different_rows":
                    try:
                        os.mkdir(f"{user_results_files_folder_path}/find_different_rows/")
                    except FileExistsError:
                        pass
                    
                    try:
                        result = file1.find_different_rows(file2)

                        different_rows_file = CSVWizard(f"{file1_filesystem_name}-{file2_filesystem_name}_different_rows", f"{user_results_files_folder_path}/find_different_rows/")
                        different_rows_file.overwrite(result, file1_encoding)
                    
                        return Response(data={"download_link":"DUMMY_LINK"}, status=status.HTTP_200_OK)
                    except Exception as e:
                        return Response(data={"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        else:
            print("invalid: ", serializer.errors)
            return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class FileDownloadView(generics.GenericAPIView):

    def get(self, request, operation, filename):
        try:
            with open(f"results_files/{request.user.username}/{operation}/{filename}.csv", "rb") as file:
                response = HttpResponse(file.read(), content_type="text/csv")
                response['Content-Disposition'] = f"attachment; filename={filename}"
                return response
        except FileNotFoundError:
            return Response(status=status.HTTP_404_NOT_FOUND)
