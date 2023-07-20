from django.urls import path
from . import views as file_views

urlpatterns = [
    path("", file_views.FilesView.as_view(), name="files_view")
]
