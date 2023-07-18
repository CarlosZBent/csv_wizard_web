from django.urls import path
from . import views as auth_views

urlpatterns = [
    path("register/", auth_views.UserCreateView.as_view(), name="register_auth"),
    path("login/", auth_views.LoginView.as_view(), name="login_auth"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout_auth"),
    path("update-user/",auth_views.UserUpdateView.as_view(), name="update-user"),
    path("update-pass/", auth_views.UserPasswordUpdateView.as_view(), name="update-pass")
]
