from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response
from . import serializers


class FilesView(generics.GenericAPIView):
    
    serializer_class = serializers.FileSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        request_data = self.request.data
        print(request_data)
        print(request.user)
        if serializer.is_valid():
            print("valid")
        else:
            print("invalid")
        return Response(status=status.HTTP_200_OK)