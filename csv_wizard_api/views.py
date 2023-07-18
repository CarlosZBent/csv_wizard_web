from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.validators import ValidationError
from django.core.validators import validate_email
from django.core.exceptions import PermissionDenied
from authentication.models import User


class UserDetailsView(generics.GenericAPIView):

    def get(self, request, email):

        if not email:
            raise ValidationError(detail="Email Parameter Missing", code=status.HTTP_422_UNPROCESSABLE_ENTITY)
        elif validate_email(email) == None:
            authenticated_user = request.user
            if authenticated_user.email == email:
                user = User.objects.filter(email=email).first()
                return Response(data={
                    "username":user.username,
                    "email":user.email
                })
            else:
                raise PermissionDenied
                # should also send an alert to admin