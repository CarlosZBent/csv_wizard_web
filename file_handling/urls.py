from django.urls import path
from . import views as file_views

urlpatterns = [
    path("files/", file_views.FilesView.as_view(), name="files_view")
]
