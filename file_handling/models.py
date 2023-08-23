from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class File(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    size = models.FloatField()
    name = models.CharField(max_length=250)
    is_deleted = models.BooleanField()
    # operation_name will never be default, this default value is for records that were created before adding this field
    operation_name = models.CharField(max_length=25, default="no_operation_defined")
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"File {self.name} - {self.created_at}"
