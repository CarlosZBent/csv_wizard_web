from django.urls import path
from . import views as file_views

urlpatterns = [
    path("", file_views.FilesView.as_view(), name="files_view"),    
    path("download/<operation>/<filename>", file_views.FileDownloadView.as_view(), name="file_download_view"),    
]
