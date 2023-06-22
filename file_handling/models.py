from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class File(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    size = models.CharField(max_length=50)
    name = models.CharField(max_length=250)
    is_deleted = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"File {self.name} - {self.created_at}"
