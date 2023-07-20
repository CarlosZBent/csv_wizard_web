from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response
from . import serializers
from .models import File


class FilesView(generics.GenericAPIView):
    
    serializer_class = serializers.FileSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        request_data = self.request.data
        print(request_data)
        print(request.user)
        if serializer.is_valid():
            print("valid")
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
            return Response({"error": serializer.error}, status=status.HTTP_400_BAD_REQUEST)