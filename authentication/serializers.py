from .models import User
from rest_framework.validators import ValidationError
from rest_framework import serializers

from django.contrib.auth import authenticate, login


class UserCreationSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=25)
    email = serializers.EmailField(max_length=80)
    password = serializers.CharField(min_length=8)

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'password'
        ]

        def validate(self, attrs):
            username_exists = User.objects.filter(username=attrs.get('username')).exists()

            if username_exists:
                print('username already exists')
                raise ValidationError(detail='username already exists')

            email_exists = User.objects.filter(username=attrs.get('email')).exists()

            if email_exists:
                print('email already exists')
                raise ValidationError(detail='email already exists')


            return super().validate(attrs)

class UserUpdateSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=25)
    email = serializers.EmailField(max_length=80)

    class Meta:
        model = User
        fields = [
            'username',
            'email',
        ]

        def validate(self, attrs):
            return super().validate(attrs)
            

class UserPasswordUpdateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(min_length=8)

    class Meta:
        model = User
        fields = [
            'password'
        ]

        def validate(self, attrs):
            return super().validate(attrs)


class LoginSerializer(serializers.Serializer):

    username = serializers.CharField(label="Username", write_only=True)
    password = serializers.CharField(label="Password", style={'input_type': 'password'}, trim_whitespace=False, write_only=True)

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        if username and password:
            user = User.objects.filter(username=username).first()
            print("user:", user)
            print("authenticate:", authenticate(self.context.get("request"), username=username, password=password))
            
            if not user:
                msg = 'Access denied: wrong username or password.'
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = 'Both "username" and "password" are required.'
            raise serializers.ValidationError(msg, code='authorization')        

        attrs['user'] = user
        return attrs
