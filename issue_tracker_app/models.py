from django.db import models

# Create your models here.

from django.db import models
from django.utils import timezone


class User(models.Model):
    user_id = models.UUIDField(primary_key=True)
    username = models.CharField(max_length=15, null=False)
    password = models.TextField(null=False)
    created_at = models.DateTimeField(default=timezone.now())
    last_modified = models.DateTimeField(blank=True, null=True)

    def create_new_user(self):
        self.last_modified = timezone.now()
        self.save()

    def __str__(self):
        return f"app_users_model"
