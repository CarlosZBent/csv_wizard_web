from django.shortcuts import render
from rest_framework import generics, status, views, permissions
from rest_framework.response import Response
from django.contrib.auth import login, authenticate
from .models import User
from . import serializers


class UserCreateView(generics.GenericAPIView):
    
    serializer_class = serializers.UserCreationSerializer

    permission_classes = (permissions.AllowAny, )

    def post(self, request):

        serializer = self.serializer_class(data=request.data)

        try:
            if serializer.is_valid():
                serializer.save()
                print('>>> SERIALIZER IS VALID')
                return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response(data={ "error":str(e) }, status=status.HTTP_400_BAD_REQUEST)


class LoginView(generics.GenericAPIView):

    serializer_class = serializers.LoginSerializer

    permission_classes = (permissions.AllowAny, )

    def post(self, request, format=None):
        serializer = self.serializer_class(data=self.request.data, context={ 'request': self.request })
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        print(login(request, user))
        print("is auth:", self.request.user.is_authenticated)
        return Response(None, status.HTTP_202_ACCEPTED)
