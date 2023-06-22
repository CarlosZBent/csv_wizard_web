from django.urls import path
from . import views as auth_views

urlpatterns = [
    path("register/", auth_views.UserCreateView.as_view(), name="register_auth")
]
