from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response


class FilesView(generics.GenericAPIView):
    def get(self, request):
        return Response(data= { "message":"HELLO files" }, status=status.HTTP_200_OK)


class FilesView(generics.GenericAPIView):
    def get(self, request):
        return Response(data= { "message":"HELLO files" }, status=status.HTTP_200_OK)