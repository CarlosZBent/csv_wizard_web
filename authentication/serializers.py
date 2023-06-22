from .models import User
from rest_framework import serializers
from rest_framework.validators import ValidationError


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
            print(">>> VALIDATE()")
            username_exists = User.objects.filter(username=attrs.get('username')).exists()

            if username_exists:
                print('username already exists')
                raise ValidationError(detail='username already exists')

            email_exists = User.objects.filter(username=attrs.get('email')).exists()

            if email_exists:
                print('email already exists')
                raise ValidationError(detail='email already exists')


            return super().validate(attrs)
