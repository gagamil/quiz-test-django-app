from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    ROLE_ADMINISTRATOR = 1
    ROLE_SIMPLE = 2
    ROLE_CHOICES = (
        (ROLE_ADMINISTRATOR, 'Administrator'),
        (ROLE_SIMPLE, 'Simple user')
    )

    role = models.IntegerField(choices=ROLE_CHOICES)