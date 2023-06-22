from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager
from django.db import models
from django.utils.translation import gettext_lazy as _

class CustomUserManager(BaseUserManager):
    def create_user(self, username, email, password, **extra_fields):
        if not email:
            raise ValueError(_("no email found"))

        email = self.normalize_email(email)
        username = username

        new_user = self.model(email=email, username=username, **extra_fields)
        new_user.set_password(password)
        new_user.save()

        return new_user

    def create_superuser(self, username, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") != True:
            raise ValueError('not staff')
        if extra_fields.get("is_superuser") != True:
            raise ValueError('not superuser')
        if extra_fields.get("is_active") != True:
            raise ValueError('not active')

        return self.create_user(username, email, password, **extra_fields)


class User(AbstractUser):
    username = models.CharField(max_length=25, unique=True)
    email = models.EmailField(max_length=80, unique=True)

    REQUIRED_FIELDS = ['email']
    USERNAME_FIELD = 'username'

    objects = CustomUserManager()

    def __str__(self):
        return f"User {self.username} - {self.email}"