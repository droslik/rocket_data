from django.contrib.auth.models import AbstractUser
from django.db import models
from entities.models import Entity
from rest_framework_api_key.models import AbstractAPIKey


class User(AbstractUser):
    role = models.CharField(max_length=10, default='user')
    entity = models.ForeignKey(
        Entity,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='users'
    )


class UserAPIKey(AbstractAPIKey):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="api_keys",
    )

