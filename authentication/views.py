from django.shortcuts import render
from rest_framework import generics, status, views, permissions
from rest_framework.response import Response
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.hashers import make_password
from .models import User
from . import serializers


class UserCreateView(generics.GenericAPIView):
    
    serializer_class = serializers.UserCreationSerializer

    permission_classes = (permissions.AllowAny, )

    def post(self, request):

        serializer = self.serializer_class(data=request.data)

        try:
            if serializer.is_valid():
                user = User.objects.create_user(**serializer.validate(self.request.data))
                return Response(data={
                    "username": self.request.data.get("username"), 
                    "email":self.request.data.get("email")
                    }, 
                    status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response(data={ "error":str(e) }, status=status.HTTP_400_BAD_REQUEST)



class UserUpdateView(generics.GenericAPIView):

    serializer_class = serializers.UserUpdateSerializer


    def put(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            authenticated_user = request.user
            user = User.objects.filter(email=authenticated_user.email).first()
            user.email = self.request.data.get("email")
            user.username = self.request.data.get("username")
            user.save()
            authenticate(
                request = self.request,
                username = self.request.data.get("username"),
                password = user.password
                )
            login(self.request, user)
            return Response(data={
                "username": self.request.data.get("username"), 
                "email":self.request.data.get("email")
                },
                status=status.HTTP_202_ACCEPTED)


class UserPasswordUpdateView(generics.GenericAPIView):

    serializer_class = serializers.UserPasswordUpdateSerializer

    def put(self, request):
        serializer = self.serializer_class(data=request.data)

        new_password = self.request.data.get("password")
        
        authenticated_user = request.user
        user = User.objects.filter(username=authenticated_user.username, email=authenticated_user.email).first()
        user.password = make_password(new_password)
        user.save()
        logout(self.request)
        return Response(data={"password_updated":user.username}, status=status.HTTP_202_ACCEPTED)


class LoginView(generics.GenericAPIView):

    serializer_class = serializers.LoginSerializer

    permission_classes = (permissions.AllowAny, )

    def post(self, request, format=None):
        serializer = self.serializer_class(data=self.request.data, context={ 'request': self.request })
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        print("login:", login(request, user))
        print("is auth:", self.request.user.is_authenticated)
        return Response(None, status.HTTP_202_ACCEPTED)


class LogoutView(generics.GenericAPIView):

    def get(self, request):
        logout(self.request)
        return Response(status=status.HTTP_200_OK)
