from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response
from .models import User
from . import serializers


class UserCreateView(generics.GenericAPIView):
    
    serializer_class = serializers.UserCreationSerializer

    def post(self, request):

        serializer = self.serializer_class(data=request.data)

        """
        if serializer.is_valid():
            print('>>> SERIALIZER IS VALID')
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)

        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        """

        try:
            if serializer.is_valid():
                serializer.save()
                print('>>> SERIALIZER IS VALID')
                return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response(data={ "error":str(e) }, status=status.HTTP_400_BAD_REQUEST)
